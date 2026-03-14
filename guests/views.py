from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.timezone import localtime
from django.contrib import messages
from django.db.models import Count, Q
from .models import Guest
from .forms import CheckInForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.core.paginator import Paginator
import random
import string


def dashboard_view(request):
    stats = Guest.objects.aggregate(
        total=Count("id"),
        checked_in=Count("id", filter=Q(checkin=True)),
        not_checked_in=Count("id", filter=Q(checkin=False)),
    )
    return render(request, "guests/dashboard.html", {"stats": stats})

def desk_view(request, desk_id: int):
    form = CheckInForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        q = form.cleaned_data["query"].strip()

        guest = Guest.objects.filter(invitation_code__iexact=q).first() or \
                Guest.objects.filter(name__iexact=q).first()

        if not guest:
            messages.error(request, "Guest not found.")
            return redirect(request.path)

        # Duplicate guard
        if guest.checkin:
            messages.warning(request, f"{guest.name} already checked-in at {guest.checkin_at:%H:%M}.")
            return redirect(request.path)

        # Mark check-in
        guest.checkin = True
        guest.checkin_at = timezone.now()
        guest.desk_id = desk_id
        guest.screen_id = desk_id          # simple 1-to-1 mapping
        guest.save()

        # Push event to screen
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"screen_{guest.screen_id}",
            {
                "type": "group.message",
                "text": guest.name,
                "status": guest.status,
            },
        )

        # Store guest detail in session so it survives the redirect
        request.session['last_checkin'] = {
            'name': guest.name,
            'status': guest.get_status_display(),
            'detail': guest.detail,
            'invitation_code': guest.invitation_code,
            'checkin_at': localtime(guest.checkin_at).strftime('%H:%M'),
        }

        messages.success(request, f"Welcome {guest.name}!")
        return redirect(request.path)

    last_checkin = request.session.pop('last_checkin', None)
    return render(request, "guests/desk.html", {"form": form, "desk_id": desk_id, "last_checkin": last_checkin})


def walk_in_view(request, desk_id: int):
    """Tambah tamu walk-in (tidak terdaftar) langsung dari desk."""
    if request.method != "POST":
        return redirect("guests:desk", desk_id=desk_id)

    name   = request.POST.get("name", "").strip()
    detail = request.POST.get("detail", "").strip()

    if not name:
        messages.error(request, "Nama tamu tidak boleh kosong.")
        return redirect("guests:desk", desk_id=desk_id)

    # Generate unique invitation code: WI-XXXXXX
    def gen_code():
        return "WI-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    code = gen_code()
    while Guest.objects.filter(invitation_code=code).exists():
        code = gen_code()

    now = timezone.now()
    guest = Guest.objects.create(
        name=name,
        detail=detail,
        invitation_code=code,
        status=Guest.Status.REGULER,
        checkin=True,
        checkin_at=now,
        desk_id=desk_id,
        screen_id=desk_id,
    )

    # Push ke screen
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"screen_{guest.screen_id}",
        {"type": "group.message", "text": guest.name, "status": guest.status},
    )

    request.session["last_checkin"] = {
        "name": guest.name,
        "status": guest.get_status_display(),
        "detail": guest.detail,
        "invitation_code": guest.invitation_code,
        "checkin_at": localtime(now).strftime("%H:%M"),
    }

    messages.success(request, f"Tamu walk-in {guest.name} berhasil ditambahkan & check-in.")
    return redirect("guests:desk", desk_id=desk_id)


def screen_view(request, screen_id: int):
    # Sebentar: template kosong, nanti di Tahap 5
    return render(request, "guests/screen.html", {"screen_id": screen_id})

def api_guest_search(request):
    q = request.GET.get('q', '').strip()
    if not q:
        return JsonResponse({'results': []})
    guests = Guest.objects.filter(name__icontains=q).order_by('name')[:10]
    results = [
        {
            'id': str(g.id),
            'name': g.name,
            'invitation_code': g.invitation_code,
            'status': g.status,
            'detail': g.detail,
        }
        for g in guests
    ]
    return JsonResponse({'results': results})

def guest_list_view(request):
    sort = request.GET.get('sort', 'name')
    dir = request.GET.get('dir', 'asc')
    valid_cols = ['name', 'invitation_code', 'status', 'checkin', 'checkin_at', 'desk_id', 'detail']
    if sort not in valid_cols:
        sort = 'name'
    order = sort if dir == 'asc' else f'-{sort}'
    guests = Guest.objects.all().order_by(order)
    paginator = Paginator(guests, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'guests/guest_list.html', {
        'page_obj': page_obj,
        'sort': sort,
        'dir': dir,
        'valid_cols': valid_cols,
    })

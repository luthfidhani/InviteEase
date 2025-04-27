from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count, Q
from .models import Guest
from .forms import CheckInForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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

        messages.success(request, f"Welcome {guest.name}!")
        return redirect(request.path)

    return render(request, "guests/desk.html", {"form": form, "desk_id": desk_id})


def screen_view(request, screen_id: int):
    # Sebentar: template kosong, nanti di Tahap 5
    return render(request, "guests/screen.html", {"screen_id": screen_id})

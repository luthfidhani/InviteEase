from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportMixin
from .models import Guest


@admin.register(Guest)
class GuestAdmin(ImportExportMixin, ExportMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "invitation_code",
        "status",
        "checkin",
        "checkin_at",
        "desk_id",
        "screen_id",
    )
    list_filter = ("status", "checkin")
    search_fields = ("name__icontains", "invitation_code__icontains")
    ordering = ("name",)

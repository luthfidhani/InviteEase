import uuid
from django.db import models

class Guest(models.Model):
    class Status(models.TextChoices):
        VVIP = "vvip", "VVIP"
        VIP = "vip", "VIP"
        REGULER = "reguler", "Reguler"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    invitation_code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.REGULER,
    )
    checkin = models.BooleanField(default=False)
    checkin_at = models.DateTimeField(null=True, blank=True)
    desk_id = models.PositiveSmallIntegerField(null=True, blank=True)
    screen_id = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["checkin"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.id})"

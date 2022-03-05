from uuid import uuid4

from django.db import models
from django.db.models.functions import Now
from django.contrib.auth import get_user_model


class OtpManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(created_at__lt=Now())


class Otp(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid4,
    )
    otp = models.PositiveIntegerField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="otps",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = OtpManager()

    def __str__(self):
        return f"{self.otp} -> ({self.user.username}, {self.user.phone})"

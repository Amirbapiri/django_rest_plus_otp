from uuid import uuid4
from django.db import models

from django.contrib.auth import get_user_model


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

    def __str__(self):
        return f"{self.otp} -> ({self.user.username}, {self.user.phone})"

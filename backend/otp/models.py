import datetime

from uuid import uuid4

from django.db import models
from django.db.models.functions import Now
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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.otp} -> ({self.user.username}, {self.user.phone})"

    def is_expired(self):
        current_time = datetime.datetime.now().astimezone()
        time_to_keep_in_seconds = 300  ## 5 minutes
        diff = current_time - self.created_at
        if diff.seconds > time_to_keep_in_seconds:
            return True
        return False

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

from accounts.utils import phone_validator


class UserManager(BaseUserManager):
    def _create_user(self, username, phone, password=None, **extra_fields):
        if not username:
            raise ValueError("users must have a unique 'username'.")
        if not phone:
            raise ValueError("users must have a unique 'phone'.")
        user = self.model(username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            username=username,
            phone=phone,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, username, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            username=username,
            phone=phone,
            password=password,
            **extra_fields,
        )


class User(AbstractUser):
    email = None
    # add phone validator
    phone = models.CharField(
        max_length=11,
        unique=True,
        blank=False,
        null=False,
        validators=[phone_validator],
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone"]
    backend = "accounts.backends.OTPBackend"

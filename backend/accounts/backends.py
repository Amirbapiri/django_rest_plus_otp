from django.shortcuts import get_object_or_404
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model


User = get_user_model()


class OTPBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        phone = request.data.get("phone")
        if phone:
            user = get_object_or_404(User, phone=phone)
            return user
        return None

    def get_user(self, user_id: int):
        try:
            return get_object_or_404(User, pk=user_id)
        except User.DoesNotExist:
            return None

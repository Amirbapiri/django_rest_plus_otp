import datetime

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework import status, permissions, response
from rest_framework import generics, views

from rest_framework_simplejwt.tokens import Token

from otp.models import Otp
from .serializers import UserRegistrationSerializer
from coreapi.utils import otp_generator, send_otp


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.set_password(self.request.data.get("password"))
        obj.save()


class CreateTokenManually:
    @classmethod
    def access(self, user):
        Token.token_type = "access"
        Token.lifetime = datetime.timedelta(hours=3)
        return Token.for_user(user)

    @classmethod
    def refresh(self, user):
        Token.token_type = "refresh"
        Token.lifetime = datetime.timedelta(hours=5)
        return Token.for_user(user)


class UserOTPLogin(views.APIView):
    permission_classes = [permissions.AllowAny]

    def remove_expired_otp(self, otp):
        pass

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        if phone:
            user = get_object_or_404(get_user_model(), phone=phone)
            otp = user.otps.first()
            if otp:
                if otp.is_expired():
                    otp.delete()
                    otp = otp_generator()
                    Otp.objects.create(user=user, otp=otp)
                send_otp(user.phone, otp)
                return response.Response(
                    {"created": True},
                    status=status.HTTP_201_CREATED,
                    headers={"Location": reverse_lazy("api:accounts:verify")},
                )
            # generate token and SMS to user
            otp = otp_generator()
            Otp.objects.create(user=user, otp=otp)
            send_otp(user.phone, otp)
            return response.Response(
                {"created": True},
                status=status.HTTP_201_CREATED,
                headers={"Location": reverse_lazy("api:accounts:verify")},
            )


class OTPverify(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            otp = get_object_or_404(Otp, otp=request.data.get("otp"))
            if otp:
                access_token = CreateTokenManually.access(otp.user)
                refresh_token = CreateTokenManually.refresh(otp.user)
                return response.Response(
                    {"access": str(access_token), "refresh": str(refresh_token)}
                )
            return response.Response({"detail": "Invalid token"})
        except Otp.DoesNotExist:
            return response.Response({"detail": "The code you've typed is invalid."})

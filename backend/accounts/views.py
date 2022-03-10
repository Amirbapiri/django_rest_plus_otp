from datetime import datetime
from http.client import responses

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework import status, permissions, response
from rest_framework import generics, views
from rest_framework_simplejwt.tokens import Token
from redis import Redis, WatchError

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

    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_HASH_NAME = "otp"

    def remove_expired_otp(self, otp):
        pass

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        user_exists = get_user_model().objects.filter(phone=phone).exists()
        if not user_exists:
            return response.Response(
                {"detail": f"No user found with phone: {phone}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        r = Redis(host=self.REDIS_HOST, port=self.REDIS_PORT, db=self.REDIS_DB)
        otp = otp_generator()
        # example: 9011011100
        identifier = phone[1:]
        with r.pipeline() as pipe:
            try:
                pipe.watch(identifier)
                if not pipe.exists(identifier):
                    pipe.multi()
                    pipe.set(otp, value=otp, ex=180)
                    pipe.hmset(identifier, {"status": 1})
                    pipe.expire(identifier, time=180)
                    pipe.execute()
                    send_otp(phone, otp)
                    return response.Response(
                        {"created": True},
                        status=status.HTTP_201_CREATED,
                        headers={"Location": reverse_lazy("api:accounts:verify")},
                    )
                return response.Response(
                    {"detail": f"OTP already exists for {phone}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            finally:
                pipe.reset()


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

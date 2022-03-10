import datetime
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

    def __init__(self):
        self.client = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
        )
        super().__init__()

    def does_user_exists(self, phone):
        user_exists = get_user_model().objects.filter(phone=phone).exists()
        return user_exists

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone")
        if not self.does_user_exists(phone):
            return response.Response(
                {"detail": f"No user found with phone: {phone}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        otp = otp_generator()
        # example: 9011011100
        identifier = phone[1:]
        with self.client.pipeline() as pipe:
            try:
                pipe.watch(identifier)
                if not pipe.exists(identifier):
                    pipe.multi()
                    pipe.hmset(otp, {"phone": phone})
                    pipe.expire(otp, time=180)
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
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_HASH_NAME = "otp"

    def __init__(self, **kwargs):
        self.client = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
        )
        super().__init__(**kwargs)

    def post(self, request, *args, **kwargs):
        phone = self.client.hget(request.data.get("otp"), "phone").decode()
        user = get_object_or_404(get_user_model(), phone=phone)
        access_token = CreateTokenManually.access(user)
        refresh_token = CreateTokenManually.refresh(user)
        print(access_token)
        return response.Response(
            {"access": str(access_token), "refresh": str(refresh_token)}
        )

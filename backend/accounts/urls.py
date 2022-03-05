from django.urls import path

from .views import UserRegistrationView, UserOTPLogin, OTPverify

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("otp/login/", UserOTPLogin.as_view(), name="login"),
    path("otp/verify/", OTPverify.as_view(), name="verify"),
]

from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # accounts OTP authentication
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    # Token Authentication
    path("auth/", obtain_auth_token),
    # JWT authentication
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # products
    path("products/", include(("products.urls", "products"), namespace="products")),
    # search
    path("search/", include(("search.urls", "search"), namespace="search")),
]

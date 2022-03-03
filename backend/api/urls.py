from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("auth/", obtain_auth_token),
    # products
    path("products/", include(("products.urls", "products"), namespace="products")),
    # search
    path("search/", include(("search.urls", "search"), namespace="search")),
]

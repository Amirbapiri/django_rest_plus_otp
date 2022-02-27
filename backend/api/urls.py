from django.urls import path

from api.views import get_products

urlpatterns = [
    path("products/all/", get_products, name="all_products"),
]

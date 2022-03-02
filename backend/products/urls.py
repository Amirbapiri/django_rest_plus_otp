from django.urls import path

from products.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
)


urlpatterns = [
    path("", ProductListCreateAPIView.as_view(), name="list"),
    path("new/", ProductListCreateAPIView.as_view(), name="create"),
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("<int:pk>/update/", ProductUpdateAPIView.as_view(), name="product_update"),
    path("<int:pk>/delete/", ProductDeleteAPIView.as_view(), name="product_delete"),
]

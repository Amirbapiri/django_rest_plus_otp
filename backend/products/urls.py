from django.urls import path

from products.views import ProductDetailAPIView

urlpatterns = [
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
]

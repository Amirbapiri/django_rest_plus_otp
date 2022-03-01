from django.urls import path

from products.views import ProductCreateAPIView, ProductDetailAPIView

urlpatterns = [
    path("<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path("new/", ProductCreateAPIView.as_view(), name="create"),
]

from rest_framework.generics import RetrieveAPIView, CreateAPIView

from api.serializers import ProductSerializer

from .models import Product


class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(pk=self.kwargs.get("pk"))
        return qs

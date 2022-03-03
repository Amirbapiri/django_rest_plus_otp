from rest_framework import generics, permissions

from products.models import Product
from products.serializers import ProductSerializer


class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            qs = super().get_queryset()
            user = self.request.user
            if user.is_authenticated:
                return qs.search(query, user=user)
            return qs.search(query)
        return Product.objects.none()

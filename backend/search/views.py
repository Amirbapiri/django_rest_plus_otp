from rest_framework import generics, permissions, response, status

from products.models import Product
from products.serializers import ProductSerializer

from . import client


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


class SearchAlgoliaListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        is_public = str(request.GET.get("is_public")) != 0
        tag = request.GET.get("tag")
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        if not query:
            response.Response("", status=status.HTTP_404_NOT_FOUND)
        result = client.perform_search(
            query,
            tags=tag,
            user=user,
            is_public=is_public,
        )
        return response.Response(result)

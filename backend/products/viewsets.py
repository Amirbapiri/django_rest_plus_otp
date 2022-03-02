from rest_framework import viewsets, mixins

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    """
    GET -> Retrieve all
    GET -> Detail
    POST -> Create
    PUT -> Update
    PATCH -> Partial Update
    delete -> destory
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = "pk"


class ProductGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET -> Retrieve all
    GET -> Detail
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_fields = "pk"

from rest_framework import permissions, authentication
from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    mixins,
    GenericAPIView,
)

from api.serializers import ProductSerializer
from api.authentication import TokenAuthentication
from api.permissions import IsStaffEditorPermissions

from .models import Product


class ProductMixinView(mixins.ListModelMixin, GenericAPIView):
    """
    It is similar to ListAPIView. Here purpose is to illustrate that we can
    create our own custom generic thanks to mixins.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductListDetailView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermissions]
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication,
    ]

    def perform_create(self, serializer):
        """
        content field is already set to be considered as a required field
        so if you don't set, you will get:
        {
            "content": [
                "This field is required."
            ]
        }
        if you set it to an empty value:
            {
                "content": [
                    "This field may not be blank."
                ]
            }
        """
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = title
        serializer.save()


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(pk=self.kwargs.get("pk"))
        return qs


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermissions]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            instance.save()
        return instance


class ProductDeleteAPIView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermissions]

    def perform_destory(self, instance):
        # Do whatever you want with the instance that is going to be removed.
        super().perform_destroy(instance)

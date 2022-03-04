from rest_framework import authentication
from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    mixins,
    GenericAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductSerializer
from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin, UserQuerysetMixin

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


class ProductListCreateAPIView(
    StaffEditorPermissionMixin, UserQuerysetMixin, ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication,
        JWTAuthentication,
    ]
    ALLOW_STAFF_VIEW = False

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
        serializer.save(user=self.request.user)

    # def get_queryset(self, *args, **kwargs):
    #     # We're going to create a mixin for code reduction here
    #     request = self.request
    #     # if not request.user.is_authenticated:
    #     #     return Product.objects.none()
    #     qs = super().get_queryset(*args, **kwargs)
    #     return qs.filter(user=request.user)


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(pk=self.kwargs.get("pk"))
        return qs


class ProductUpdateAPIView(StaffEditorPermissionMixin, UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            instance.save()
        return instance


class ProductDeleteAPIView(
    StaffEditorPermissionMixin, UserQuerysetMixin, DestroyAPIView
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def perform_destory(self, instance):
        # Do whatever you want with the instance that is going to be removed.
        super().perform_destroy(instance)

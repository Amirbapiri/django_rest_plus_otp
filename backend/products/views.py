from rest_framework.generics import (
    RetrieveAPIView,
    ListCreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)

from api.serializers import ProductSerializer

from .models import Product


class ProductCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []

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
    permission_classes = []

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            instance.save()
        return instance


class ProductDeleteAPIView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = []

    def perform_destory(self, instance):
        # Do whatever you want with the instance that is going to be removed.
        super().perform_destroy(instance)

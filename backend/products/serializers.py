from rest_framework import serializers, status
from rest_framework.reverse import reverse

from products.models import Product
from products.validators import (
    validate_title,
    validate_title_no_junky_words,
    unique_product_validator,
)
from api.serializers import UserPublicSerializer


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:products:product_detail",
        lookup_field="pk",
        read_only=True,
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    related_products = ProductInlineSerializer(
        source="user.products.all", read_only=True, many=True
    )
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="api:products:product_detail", lookup_field="pk"
    )
    # email = serializers.EmailField(write_only=True)
    title = serializers.CharField(
        validators=[
            unique_product_validator,
            validate_title,
            validate_title_no_junky_words,
        ]
    )
    # name = serializers.CharField(source="title", read_only=True)
    # creator = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Product
        fields = [
            "url",
            "edit_url",
            # "user",
            "owner",
            # "creator",
            "related_products",
            "title",
            # "name",
            "content",
            "price",
            "sale_price",
            "title_in_uppercase",
            "discount",
            # "email",
        ]

    def get_discount(self, obj):
        if obj.discount():
            return obj.discount()
        return "NO COUPON"

    def get_edit_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse(
            "api:products:product_update",
            kwargs={"pk": obj.pk},
            request=request,
        )

    # def create(self, validated_data):
    #     email = validated_data.pop("email")
    #     # Doing something with email
    #     return super().create(validated_data)

    # def validate_title(self, value):
    #     request = self.context.get("request")
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(
    #             detail=f"'{value}' is already a product title.",
    #             code=status.HTTP_400_BAD_REQUEST,
    #         )
    #     return value

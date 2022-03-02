from rest_framework import serializers
from rest_framework.reverse import reverse

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="api:products:product_detail", lookup_field="pk"
    )

    class Meta:
        model = Product
        fields = [
            "url",
            "edit_url",
            "title",
            "content",
            "price",
            "sale_price",
            "title_in_uppercase",
            "discount",
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

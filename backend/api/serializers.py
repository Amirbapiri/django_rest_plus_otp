from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
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

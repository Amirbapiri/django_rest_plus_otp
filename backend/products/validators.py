from rest_framework import serializers, status

from .models import Product


def validate_title(value):
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(
            detail=f"'{value}' is already a product title.",
            code=status.HTTP_400_BAD_REQUEST,
        )
    return value

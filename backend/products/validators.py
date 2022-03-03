from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from .models import Product


def validate_title(value):
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(
            detail=f"'{value}' is already a product title.",
            code=status.HTTP_400_BAD_REQUEST,
        )
    return value


def validate_title_no_junky_words(value):
    """
    this methods validates value to check if there is something like:
    "hello", "goodbye" or similar junky words.
    """
    junky_words = ["hello", "bye", "hi"]
    if value.lower() in junky_words:
        raise serializers.ValidationError(
            detail=f"'{value}' is a junky word to be in title",
            code=status.HTTP_400_BAD_REQUEST,
        )
    return value


unique_product_validator = UniqueValidator(
    queryset=Product.objects.all(), lookup="iexact"
)

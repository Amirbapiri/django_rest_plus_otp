from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.serializers import ProductSerializer
from products.models import Product


@api_view(http_method_names=["GET"])
def get_products(request):
    instance = Product.objects.all().order_by("?").first()
    if instance:
        serialized_data = ProductSerializer(instance).data
        return Response(serialized_data)
    return Response({"error": "There is no product there!"})

from rest_framework.routers import DefaultRouter

from products.viewsets import ProductGenericViewSet, ProductViewSet


router = DefaultRouter()
# router.register("products-abc", ProductViewSet, basename="products")
router.register("product-abc", ProductGenericViewSet, basename="products")

urlpatterns = router.urls

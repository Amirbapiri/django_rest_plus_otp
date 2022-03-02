from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # DRF
    path("api-auth/", include("rest_framework.urls")),
    # api
    path("api/", include(("api.urls", "api"), namespace="api")),
    path("api/v2/", include(("coreapi.routers", "coreapi"), namespace="api_v2")),
]

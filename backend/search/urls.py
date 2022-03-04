from django.urls import path

from .views import SearchListView, SearchAlgoliaListView

urlpatterns = [
    path("", SearchListView.as_view(), name="search"),
    path("algolia/", SearchAlgoliaListView.as_view(), name="search_algolia"),
]

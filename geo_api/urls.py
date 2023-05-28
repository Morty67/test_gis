from django.urls import include, path
from rest_framework import routers

from geo_api.views import PlaceViewSet


router = routers.DefaultRouter()
router.register("places", PlaceViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "nearest-place/",
        PlaceViewSet.as_view({"get": "get_nearest_place"}),
        name="nearest-place",
    ),
]

app_name = "geo"

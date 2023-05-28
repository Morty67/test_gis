from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Place
from .serializers import PlaceSerializer
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self):
        """
        Returns the queryset of all Place objects.
        """
        queryset = super().get_queryset()
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Returns a list of all Place objects.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Creates a new Place object.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieves details of a specific Place object by its identifier (id).
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Updates a specific Place object by its identifier (id).
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates a specific Place object by its identifier (id).
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a specific Place object by its identifier (id).
        """
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="latitude",
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                description="Latitude coordinate (ex. ?latitude=6.4474)",
                required=True,
            ),
            OpenApiParameter(
                name="longitude",
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                description="Longitude coordinate (ex. ?latitude=2.5241)",
                required=True,
            ),
        ],
        responses={200: PlaceSerializer},
        description="Get the nearest place to a given point",
    )
    @action(detail=False, methods=["GET"])
    def get_nearest_place(self, request):
        """
        Retrieves the nearest Place to a given point based on latitude and longitude coordinates.

        Args:
            request: The request object containing the latitude and longitude parameters.

        Returns:
            Response: The serialized data of the nearest Place.

        Raises:
            ValueError: If the latitude or longitude is invalid.

        """
        latitude = request.GET.get("latitude")
        longitude = request.GET.get("longitude")

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid coordinates"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_location = Point(longitude, latitude, srid=4326)

        nearest_place = (
            Place.objects.annotate(distance=Distance("geom", user_location))
            .order_by("distance")
            .first()
        )

        serializer = self.serializer_class(nearest_place)
        return Response(serializer.data)

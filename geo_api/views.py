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
        queryset = super().get_queryset()
        return queryset

    @action(detail=False, methods=["POST"])
    def create_place(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            place = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def get_nearest_place(self, request):
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

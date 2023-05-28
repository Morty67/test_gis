from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from geo_api.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    geom = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=Place.objects.all(),
                message="This coordinate already exists.",
            )
        ]
    )

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")

    def validate_geom(self, value):
        try:
            geom = GEOSGeometry(value)
        except (ValueError, TypeError) as e:
            raise serializers.ValidationError("Invalid geometry: " + str(e))

        if geom and not geom.empty and geom.geom_type != "Point":
            raise serializers.ValidationError("Invalid point geometry.")

        if geom and not geom.empty and (abs(geom.x) > 180 or abs(geom.y) > 90):
            raise serializers.ValidationError("Invalid coordinate range.")

        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        geom = GEOSGeometry(representation["geom"])
        representation["geom"] = geom.wkt
        return representation

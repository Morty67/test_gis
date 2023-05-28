from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from geo_api.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Place model.

    Validates and serializes the fields of a Place instance.

    """

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
        """
        Validates the geom field.

        Args:
            value (str): The value of the geom field.

        Returns:
            str: The validated geom value.

        Raises:
            serializers.ValidationError: If the geom value is invalid.

        """
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
        """
        Converts the serialized representation of the instance.

        Args:
            instance: The Place instance being serialized.

        Returns:
            dict: The serialized representation of the instance.

        """
        representation = super().to_representation(instance)
        geom = GEOSGeometry(representation["geom"])
        representation["geom"] = geom.wkt
        return representation

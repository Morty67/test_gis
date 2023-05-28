from django.test import TestCase
from geo_api.models import Place
from geo_api.serializers import PlaceSerializer


class PlaceSerializerTest(TestCase):
    def setUp(self):
        self.place_data = {
            "name": "Test Place",
            "description": "This is a test place",
            "geom": "POINT (10 20)",
        }

    def test_valid_serializer_data(self):
        """
        Test if the serializer handles valid data correctly.
        """
        serializer = PlaceSerializer(data=self.place_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_data(self):
        """
        Test if the serializer correctly identifies invalid data.
        """
        invalid_data = {
            "description": "This is an invalid place",
            "geom": "POINT (10 20)",
        }
        serializer = PlaceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("name", serializer.errors)

    def test_invalid_polygon_geom_validation(self):
        """
        Test the validation of the 'geom' field in the serializer.
        """
        invalid_data = {
            "name": "Invalid Place",
            "description": "This is an invalid place",
            "geom": "POLYGON ((0 0, 1 1, 2 2, 0 0))",
        }
        serializer = PlaceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("geom", serializer.errors)

    def test_geom_valid_coordinate_range(self):
        """
        Test the coordinate range validation in the 'geom' field.
        """
        invalid_data = {
            "name": "Invalid Place",
            "description": "This is an invalid place",
            "geom": "POINT (200 50)",
        }
        serializer = PlaceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("geom", serializer.errors)

    def test_invalid_geom_coordinate_range(self):
        """
        Test the validation of the 'geom' field when providing invalid coordinate range.
        """
        invalid_data = {
            "name": "Invalid Place",
            "description": "This is an invalid place",
            "geom": "POINT (-200 50)",
        }
        serializer = PlaceSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        self.assertIn("geom", serializer.errors)

    def test_representation(self):
        """
        Test if the serializer correctly represents the model data.
        """
        place = Place.objects.create(
            name="Test Place",
            description="This is a test place",
            geom="POINT (10 20)",
        )
        serializer = PlaceSerializer(instance=place)
        expected_representation = {
            "id": place.id,
            "name": "Test Place",
            "description": "This is a test place",
            "geom": "POINT (10 20)",
        }
        self.assertEqual(serializer.data, expected_representation)

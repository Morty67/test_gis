import re
from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APIClient
from geo_api.models import Place
from geo_api.serializers import PlaceSerializer


URL_LIST = reverse("geo:place-list")


class PlaceViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.place_data = {
            "name": "Test Place",
            "description": "This is a test place",
            "geom": "POINT (10 20)",
        }
        self.place = Place.objects.create(
            name="Existing Place",
            description="This is an existing place",
            geom="POINT (30 40)",
        )

    def test_list_places(self):
        """
        Test the listing of all places.
        """
        response = self.client.get(URL_LIST)
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_place(self):
        """
        Test the creation of a new place.
        """
        response = self.client.post(URL_LIST, data=self.place_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        place = Place.objects.get(pk=response.data["id"])
        serializer = PlaceSerializer(place)
        self.assertEqual(response.data, serializer.data)

    def test_create_place_with_invalid_data(self):
        """
        Test creating a place with invalid data.
        """
        invalid_data = {
            "name": "",
            "description": "This is a test place",
            "geom": "POINT (10 20)",
        }
        response = self.client.post(URL_LIST, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            Place.objects.filter(name=invalid_data["name"]).exists()
        )

    def test_retrieve_place(self):
        """
        Test the retrieval of a specific place.
        """
        url = reverse("geo:place-detail", args=[self.place.pk])
        response = self.client.get(url)
        serializer = PlaceSerializer(self.place)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_place(self):
        """
        Test the full update of a specific place.
        """
        url = reverse("geo:place-detail", args=[self.place.pk])
        updated_data = {
            "name": "Updated Place",
            "description": "This is an updated place",
            "geom": "POINT (50 60)",
        }
        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place.refresh_from_db()
        serializer = PlaceSerializer(self.place)
        self.assertEqual(response.data, serializer.data)

    def test_update_place_with_invalid_data(self):
        """
        Test updating a place with invalid data.
        """
        url = reverse("geo:place-detail", args=[self.place.pk])
        invalid_data = {
            "name": "",
            "description": "This is an updated place",
            "geom": "POINT (50 60)",
        }
        response = self.client.put(url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.place.refresh_from_db()
        self.assertNotEqual(self.place.name, invalid_data["name"])

    def test_partial_update_place(self):
        """
        Test the partial update of a specific place.
        """
        url = reverse("geo:place-detail", args=[self.place.pk])
        partial_data = {
            "description": "This is an updated description",
        }
        response = self.client.patch(url, data=partial_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.place.refresh_from_db()
        serializer = PlaceSerializer(self.place)
        self.assertEqual(response.data, serializer.data)

    def test_delete_place(self):
        """
        Test the deletion of a specific place.
        """
        url = reverse("geo:place-detail", args=[self.place.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Place.objects.filter(pk=self.place.pk).exists())

    def test_delete_nonexistent_place(self):
        """
        Test deleting a nonexistent place.
        """
        url = reverse("geo:place-detail", args=[9999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nearest_place(self):
        """
        Test retrieving the nearest place based on coordinates.
        """
        url = reverse("geo:place-get-nearest-place")
        query_params = {"latitude": 6.4474, "longitude": 2.5241}
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place.name)
        self.assertEqual(response.data["description"], self.place.description)

        place_geom = Point(self.place.geom.x, self.place.geom.y)
        response_geom = re.findall(r"[-+]?\d*\.\d+|\d+", response.data["geom"])
        response_geom = Point(float(response_geom[0]), float(response_geom[1]))
        self.assertEqual(response_geom, place_geom)

    def test_get_nearest_place_with_invalid_coordinates(self):
        """
        Test retrieving the nearest place with invalid coordinates.
        """
        url = reverse("geo:place-get-nearest-place")
        query_params = {"latitude": "invalid", "longitude": "coordinates"}
        response = self.client.get(url, data=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

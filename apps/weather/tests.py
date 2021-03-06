from rest_framework import status
from rest_framework.test import APITestCase

from apps.weather.models import Weather


class TestWeatherEndpoint(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = "/weather-api/weather/"

    def setUp(self):
        super().setUp()
        self.valid_data = {
            "search_lat": 50.12341,
            "search_lon": 20.12341,
            "search_type": "current",
        }
        self.invalid_data = {
            "search_lat": "",
            "search_lon": 20.12341,
            "search_type": "current",
        }
        self.no_requied_data = {
            "search_lat": 32.43231,
            "search_lon": 20.12341,
        }

    def test_endpoint_valid_data(self):
        resp = self.client.post(self.endpoint, self.valid_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Weather.objects.count(), 1)

    def test_endpoint_second_valid_post_same_data(self):
        resp = self.client.post(self.endpoint, self.valid_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Weather.objects.count(), 1)
        self.client.post(self.endpoint, self.valid_data)
        self.assertEqual(Weather.objects.count(), 1)

    def test_endpoint_invalid_data(self):
        resp = self.client.post(self.endpoint, self.invalid_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.status_text, "Bad Request")

    def test_no_data(self):
        resp = self.client.post(self.endpoint, {})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.status_text, "Bad Request")

    def test_endpoint_invalid_search_type_data(self):
        resp = self.client.post(self.endpoint, self.no_requied_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.status_text, "Bad Request")

    def test_endpoint_methods_allowance(self):
        resp = self.client.get(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.client.put(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        resp = self.client.patch(self.endpoint)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

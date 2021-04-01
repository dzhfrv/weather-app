from rest_framework import status
from rest_framework.test import APITestCase
# from .models import Weather


class TestWeatherEndpoint(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.endpoint = '/weather-api/weather/'

    def setUp(self):
        super().setUp()
        self.valid_data = {
            'search_lat': 50.12341,
            'search_lon': 20.12341,
            'search_type': 'current',
        }

        self.invalid_data = {
            'search_lat': '',
            'search_lon': 20.12341,
            'search_type': 'current',
        }

    def test_endpoint_valid_data(self):
        resp = self.client.post(self.endpoint, self.valid_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

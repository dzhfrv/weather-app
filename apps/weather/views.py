import requests

import json

from django.http import HttpResponse
from rest_framework.views import APIView

from config.settings import WEATHER_API_KEY as appkey
from .models import Weather


class WeatherView(APIView):
    def post(self, request):
        lat = request.data['search_lat']
        lon = request.data['search_lon']
        forecast_type = request.data['forecast_type']

        new_instance, created = Weather.objects.get_or_create(
            search_lat=lat,
            search_lon=lon,
            forecast_type=forecast_type,
        )
        if created:
            print('created new instance - should save data from json')
            api_link = 'http://api.openweathermap.org/data/2.5/weather'
            link = api_link + f'?lat={lat}&lon={lon}&appid={appkey}'
            response = requests.post(link)

            return HttpResponse(response)
        else:
            print('already exist - return from database')
            return HttpResponse(new_instance)

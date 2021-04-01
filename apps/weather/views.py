import requests

from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

from config.settings import (
    WEATHER_API_KEY,
    SEARCH_TIME_MINUTES,
)
from .models import Weather


class WeatherView(APIView):
    def build_link(self, lat, lon, search_type):
        api_link = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'  # noqa
        if search_type == 'current':
            link = api_link + '&exclude=minutely,hourly,daily'
        if search_type == 'minute':
            link = api_link + '&exclude=current,hourly,daily'
        if search_type == 'hourly':
            link = api_link + '&exclude=current,minutely,daily'
        if search_type == 'daily':
            link = api_link + '&exclude=current,minutely,hourly'
        return link

    def post(self, request):
        lat = request.data['search_lat']
        lon = request.data['search_lon']
        search_type = request.data['search_type']
        link = self.build_link(lat, lon, search_type)
        time = timezone.now() - timedelta(minutes=SEARCH_TIME_MINUTES)

        obj = Weather.objects.filter(
            search_lat=lat,
            search_lon=lon,
            search_type=search_type,
            search_date__gte=time,
        ).last()

        if not obj:
            try:
                response = requests.post(link)
                obj = Weather(
                    search_lat=lat,
                    search_lon=lon,
                    search_type=search_type,
                )
                obj.search_result = response.json()
                obj.save()
            except requests.exceptions.RequestException as e:
                return Response(e)
            return Response(response.json())
        else:
            data = obj.search_result
            return Response(data)

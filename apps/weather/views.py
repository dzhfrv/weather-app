from datetime import timedelta

import requests
from requests.exceptions import RequestException
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import (
    WEATHER_API_KEY,
    SEARCH_TIME_MINUTES,
)
from .models import Weather
from .serializers import WeatherEndpointDataSerializer


class WeatherView(APIView):
    def post(self, request):
        """
        POST /weather-api/weather/
        :return: JSON of the weather instance received from OpenWeatherApi
        """
        serializer = WeatherEndpointDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # receiving request params
        search_lat = request.data['search_lat']
        search_lon = request.data['search_lon']
        search_type = request.data['search_type']

        link = self.build_link(search_lat, search_lon, search_type)
        minutes = timezone.now() - timedelta(minutes=SEARCH_TIME_MINUTES)

        # __gte checks if object created 'minutes' ago
        obj = Weather.objects.filter(
            search_lat=search_lat,
            search_lon=search_lon,
            search_type=search_type,
            search_date__gte=minutes,
        ).last()

        if obj:
            # return from DB
            result = obj.search_result
            return Response(result)
        else:
            # API call
            try:
                result = self.weather_api_call(link)
                Weather.objects.create(
                    search_lat=search_lat,
                    search_lon=search_lon,
                    search_type=search_type,
                    search_result=result,
                )
                return Response(result)
            except RequestException:
                return Response(
                    'Unable to proceed with the API call',
                    status.HTTP_503_SERVICE_UNAVAILABLE
                )

    def weather_api_call(self, link):
        try:
            requests.post(link)
            result = requests.post(link).json()
            return result
        except RequestException:
            raise RequestException

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

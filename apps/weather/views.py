from datetime import timedelta

from django.utils import timezone
from requests.exceptions import RequestException
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import DATA_RELEVANCE_TIME
from .models import Weather
from .serializers import WeatherEndpointDataSerializer
from .utils import build_link, weather_api_call


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

        link = build_link(search_lat, search_lon, search_type)
        minutes = timezone.now() - timedelta(minutes=DATA_RELEVANCE_TIME)

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
                result = weather_api_call(link)
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

import json
import requests

from datetime import timedelta
from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView

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

    # def compare_dates(self, search_date):
    #     present = datetime.now()
    #     time_basis = present - timedelta(minutes=SEARCH_TIME_MINUTES)
    #     print(search_date.date() < time_basis.date())
    #     return search_date.date() < time_basis.date()

    # def postt(self, request):
    #     lat = request.data['search_lat']
    #     lon = request.data['search_lon']
    #     search_type = request.data['search_type']
    #     link = self.build_link(lat, lon, search_type)
    #     obj, created = Weather.objects.get_or_create(
    #         search_lat=lat,
    #         search_lon=lon,
    #         search_type=search_type,
    #     )
    #
    #     if created:
    #         response = requests.post(link)
    #         obj.search_result = response.json()
    #         obj.save()
    #         return HttpResponse(response)
    #     else:
    #         search_date = obj.search_date
    #         is_old_data = self.compare_dates(search_date)
    #         if is_old_data:
    #             print(1)
    #             print('data updated with - ')
    #             obj.save()
    #         else:
    #             print('not 10 minutes yet')
    #             return HttpResponse(obj)

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
            print('if not obj = TRUE, creating obj')
            obj = Weather(
                search_lat=lat,
                search_lon=lon,
                search_type=search_type,
            )
            response = requests.post(link) # вынести за создание объекта
            obj.search_result = response.json()
            obj.save()
            return HttpResponse(response)
        else:
            print('Exists - returning from db')
            data = obj.search_result
            return HttpResponse(json.dumps(data))

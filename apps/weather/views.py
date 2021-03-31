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
            api_link = 'http://api.openweathermap.org/data/2.5/weather'
            link = api_link + f'?lat={lat}&lon={lon}&appid={appkey}'
            response = requests.post(link)
            resp = response.json()
            new_instance.weather_main = resp['weather'][0]['main']
            new_instance.description = resp['weather'][0]['description']
            new_instance.temperature = resp['main']['temp']
            new_instance.feels_like = resp['main']['feels_like']
            new_instance.pressure = resp['main']['pressure']
            new_instance.humidity = resp['main']['humidity']
            new_instance.wind_speed = resp['wind']['speed']
            new_instance.save()
            # return HttpResponse(response)
            return HttpResponse(new_instance)
        else:
            #TODO если дейттайм создания записи > 10 минут, брать свежие данные
            return HttpResponse(new_instance)

        #
        # TODO: 1)добавить ссылки, проверить что json формат у ответа
        #       одинаковый, если нет - подумать о хранении респонса в jsonField
        #       2)продумать таймер ( перечитать ТЗ)
        #       3)в каком виде возвращать данные?
        #       4)валидации и тесты

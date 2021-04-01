import requests

from datetime import datetime, timedelta

from django.http import HttpResponse
from rest_framework.views import APIView

from config.settings import WEATHER_API_KEY as appkey
from .models import Weather


class WeatherView(APIView):

    def get_weather_data(self, type, lat, lon):
        print(type, lat, lon, "\n")
        link = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={appkey}'
        response = requests.post(link)
        print(response)
        resp = response.json()
        print(resp['hourly'], '\n', resp['hourly'], '\n', resp['current'], '\n')

    def post(self, request):
        lat = request.data['search_lat']
        lon = request.data['search_lon']
        forecast_type = request.data['forecast_type']

        obj, created = Weather.objects.get_or_create(
            search_lat=lat,
            search_lon=lon,
            forecast_type=forecast_type,
        )
        if created:
            self.get_weather_data(forecast_type, lat, lon)
            api_link = 'http://api.openweathermap.org/data/2.5/weather'
            link = api_link + f'?lat={lat}&lon={lon}&appid={appkey}'
            response = requests.post(link)
            resp = response.json()
            obj.weather_main = resp['weather'][0]['main']
            obj.description = resp['weather'][0]['description']
            obj.temperature = resp['main']['temp']
            obj.feels_like = resp['main']['feels_like']
            obj.pressure = resp['main']['pressure']
            obj.humidity = resp['main']['humidity']
            obj.wind_speed = resp['wind']['speed']
            obj.save()
            # return HttpResponse(response)
            return HttpResponse(obj)
        else:
            search_date = obj.search_date
            # print(search_date)
            present = datetime.now()
            timeframe = present - timedelta(minutes=10)
            # print(timeframe)
            if search_date.date() < timeframe.date():
                print('out of time')  # брать свежие данные
            else:
                print('not 10 minutes yet')  # возвращать из базы

            #TODO если дейттайм создания записи > 10 минут, брать свежие данные
            return HttpResponse(obj)

        #
        # TODO: 1)добавить ссылки, проверить что json формат у ответа
        #       одинаковый, если нет - подумать о хранении респонса в jsonField
        #       2)продумать таймер ( перечитать ТЗ)
        #       3)в каком виде возвращать данные?
        #       4)валидации и тесты

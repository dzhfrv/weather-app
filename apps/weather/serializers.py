from rest_framework import serializers
from .models import Weather


class WeatherEndpointDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        exclude = ("search_date", "search_result", )

from rest_framework import routers
from django.urls import path
from .views import WeatherView

urlpatterns = [
    path('weather/', WeatherView.as_view())
]

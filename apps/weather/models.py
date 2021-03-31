from django.db import models
from django.contrib import admin


class Weather(models.Model):

    FORECAST_TYPE = (
        (0, 'Current'),
        (1, 'Minute for 1 hour'),
        (2, 'Hourly for 48 hours'),
        (3, 'Daily  for 7 days'),
    )
    search_lat = models.FloatField()
    search_lon = models.FloatField()
    search_date = models.DateTimeField(auto_now=True)
    forecast_type = models.CharField(
        choices=FORECAST_TYPE, max_length=20, default=0)


admin.site.register(Weather)

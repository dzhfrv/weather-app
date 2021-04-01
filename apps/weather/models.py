from django.contrib import admin
from django.db import models
from django.db.models import JSONField


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
    search_type = models.CharField(
        choices=FORECAST_TYPE,
        max_length=20,
        default=0,
    )
    search_result = JSONField()

admin.site.register(Weather)


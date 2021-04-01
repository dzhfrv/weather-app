from django.contrib import admin
from django.db import models
from django.db.models import JSONField


class Weather(models.Model):
    FORECAST_TYPE = (
        ('current', 'Current'),
        ('minute', 'Minute for 1 hour'),
        ('hourly', 'Hourly for 48 hours'),
        ('daily', 'Daily  for 7 days'),
    )
    search_lat = models.FloatField()
    search_lon = models.FloatField()
    search_date = models.DateTimeField(auto_now=True)
    search_type = models.CharField(
        choices=FORECAST_TYPE,
        max_length=20,
        default=0,
    )
    search_result = JSONField(null=True, blank=True)

admin.site.register(Weather)



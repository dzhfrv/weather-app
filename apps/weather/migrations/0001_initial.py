# Generated by Django 3.1.7 on 2021-03-31 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_lat', models.FloatField()),
                ('search_lon', models.FloatField()),
                ('search_date', models.DateTimeField()),
                ('forecast_type', models.CharField(choices=[(0, 'Current'), (1, 'Minute for 1 hour'), (2, 'Hourly for 48 hours'), (3, 'Daily  for 7 days')], default=0, max_length=20)),
            ],
        ),
    ]
# Generated by Django 3.1.7 on 2021-04-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0002_auto_20210401_1308"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weather",
            name="search_type",
            field=models.CharField(
                choices=[
                    ("current", "Current"),
                    ("minute", "Minute for 1 hour"),
                    ("hourly", "Hourly for 48 hours"),
                    ("daily", "Daily  for 7 days"),
                ],
                default=0,
                max_length=20,
            ),
        ),
    ]

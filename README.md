# weather-app
_Python3, Django, Django-rest-framework, Postgres_

### .env file is required

_for receiving WEATHER_API_KEY visit: https://home.openweathermap.org/api_keys_
```dotenv
SECRET_KEY = ''
DEBUG = True
WEATHER_API_KEY = ''
DB_NAME = 'Postgres DB Name'
DB_USER = ''
DB_PWD = ''
```

### installation
* setup PostgreSQL db
  
* create `.env` file in project root
* `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirements.txt`
* `python manage.py migrate`
### request example

`http://127.0.0.1:8000/weather-api/weather/`
```json
{
    "search_type":"current",
    "search_lat": 32.213412,
    "search_lon": 20.243213
}
```
- __search_lat__ - latitude
- __search_lon__ - longitude
- __search_type__ - detailing type
  (accepts "current", "minute", "hourly" or "daily")

```
current: Current weather
minute: Minute forecast for 1 hour
hourly: Hourly forecast for 48 hours
daily: Daily forecast for 7 days
```

Data stored in DB have relevance time. The DATA_RELEVANCE_TIME setting can be found in `config/settings.py` (settled to 10 minutes by default)

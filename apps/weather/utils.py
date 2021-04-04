import requests

from config.settings import WEATHER_API_KEY


def weather_api_call(link):
    try:
        requests.post(link)
        result = requests.post(link).json()
        return result
    except requests.exceptions.RequestException as e:
        raise e


def build_link(lat, lon, search_type):
    base_url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}'  # noqa
    links_from_types = {
        'current': f'{base_url}&exclude=minutely,hourly,daily',
        'minute': f'{base_url}&exclude=current,hourly,daily',
        'hourly': f'{base_url}&exclude=current,minutely,daily',
        'daily': f'{base_url}&exclude=current,minutely,hourly',
    }
    return links_from_types.get(search_type)

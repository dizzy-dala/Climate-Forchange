import json
import urllib.parse
import urllib.request

from django.conf import settings


def get_weather_data(city=None, lat=None, lon=None):
    api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
    if not api_key:
        return {
            'error': 'OpenWeatherMap API key is not configured. Set OPENWEATHER_API_KEY in settings.'
        }

    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'appid': api_key,
        'units': 'metric',
    }

    if lat is not None and lon is not None:
        params['lat'] = lat
        params['lon'] = lon
    elif city:
        params['q'] = city
    else:
        return {'error': 'City or coordinates are required to fetch weather data.'}

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as exc:
        return {'error': f'Unable to fetch weather data: {exc}'}

    if data.get('cod') != 200:
        return {'error': data.get('message', 'Unable to fetch weather data.')}

    weather = {
        'city': data.get('name'),
        'temperature': data.get('main', {}).get('temp'),
        'humidity': data.get('main', {}).get('humidity'),
        'wind_speed': data.get('wind', {}).get('speed'),
        'description': data.get('weather', [{}])[0].get('description', ''),
        'rainfall': data.get('rain', {}).get('1h', 0) or data.get('rain', {}).get('3h', 0),
        'forecast_link': f'https://openweathermap.org/city/{data.get("id")}',
    }
    weather['advice'] = get_weather_advice(weather)
    return weather


def get_weather_advice(weather):
    if not weather or weather.get('error'):
        return ''

    advice = []
    description = (weather.get('description') or '').lower()
    temp = weather.get('temperature')
    wind = weather.get('wind_speed') or 0
    rain = weather.get('rainfall') or 0

    if rain > 0 or 'rain' in description or 'shower' in description or 'storm' in description:
        advice.append('Carry an umbrella or raincoat.')
    if 'snow' in description or 'sleet' in description or 'blizzard' in description:
        advice.append('Dress warmly and watch for slippery surfaces.')
    if temp is not None:
        if temp >= 30:
            advice.append('Stay hydrated and avoid long sun exposure.')
        elif temp <= 5:
            advice.append('Wear warm layers and protect exposed skin.')
    if wind >= 10:
        advice.append('Secure loose outdoor items and avoid exposed high areas.')
    if 'clear' in description:
        advice.append('Enjoy the clear weather, but protect your skin if you stay outside.')
    if 'cloud' in description and rain == 0:
        advice.append('Cloudy skies may stay cool, but keep an eye on local updates.')
    if not advice:
        advice.append('Weather looks stable. Stay prepared and check back later.')

    return ' '.join(advice)

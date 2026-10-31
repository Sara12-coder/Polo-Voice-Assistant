"""Chennai weather helper using Open-Meteo (no API key required)."""
import requests

# Chennai approximate coordinates
LATITUDE = 13.0827
LONGITUDE = 80.2707


def _get_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": "temperature_2m,weather_code",
        "timezone": "Asia/Kolkata",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()["current"]


def temp():
    """Return current temperature in Celsius."""
    return _get_weather()["temperature_2m"]


def des():
    """Return a readable description of the current weather."""
    code = _get_weather()["weather_code"]
    descriptions = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "slight snowfall",
        73: "moderate snowfall",
        75: "heavy snowfall",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }
    return descriptions.get(code, "weather conditions unavailable")

import requests
from app.settings import WEATHER_API_KEY

def current_weather(lat: float, lon: float):
    if not WEATHER_API_KEY:
        raise RuntimeError("WEATHER_API_KEY missing")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    return {
        "temp_c": data["main"]["temp"],
        "wind_mps": data["wind"]["speed"],
        "conditions": data["weather"][0]["description"]
    }

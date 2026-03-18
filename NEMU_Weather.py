import os
import requests
from dotenv import load_dotenv
from livekit.agents.llm import function_tool

load_dotenv('.env.local')

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5"

def _get_current_location():
    """Auto-detect current location using IP geolocation"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city'], data['country']
        return None, None, None, None
    except:
        return None, None, None, None

@function_tool(
    name="get_current_weather",
    description="Get current weather for a location. Leave city empty for current location."
)
async def get_current_weather(city: str = ""):
    try:
        if city:
            url = f"{BASE_URL}/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            lat, lon, city_name, country = _get_current_location()
            if not lat:
                return "Unable to detect location"
            url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            city = f"{city_name}, {country}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            return f"Weather in {city}: {description.capitalize()}. Temperature: {temp}°C (feels like {feels_like}°C). Humidity: {humidity}%. Wind speed: {wind_speed} m/s."
        else:
            return f"Unable to fetch weather data: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

@function_tool(
    name="get_weather_forecast",
    description="Get 5-day weather forecast for a location. Leave city empty for current location."
)
async def get_weather_forecast(city: str = ""):
    try:
        if city:
            url = f"{BASE_URL}/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        else:
            lat, lon, city_name, country = _get_current_location()
            if not lat:
                return "Unable to detect location"
            url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            city = f"{city_name}, {country}"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            forecast_list = data['list'][:40]  # 5 days * 8 entries per day
            result = f"Weather forecast for {city}:\n"
            
            current_date = None
            for item in forecast_list:
                date = item['dt_txt'].split()[0]
                
                if date != current_date:
                    current_date = date
                    temp = item['main']['temp']
                    description = item['weather'][0]['description']
                    result += f"\n{date}: {description.capitalize()}, {temp}°C"
            
            return result
        else:
            return f"Unable to fetch forecast: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {str(e)}"

# This script will notify me through SMS about today's weather condition.(it will rain or not.)

import requests
from twilio.rest import Client  # for sms
import os

MY_LAT = 37.09
MY_LONG = 150.09

Open_Weather_Map_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
MY_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# for sms
account_sid = "AC14c4d9e9d145d96aae9ab64a5ca19352"
auth_token = os.getenv("sms_auth_token")

weather_parameters = {
    'lat': MY_LAT,
    'lon': MY_LONG,
    'appid': MY_API_KEY,
    'cnt': 4,
}

# for 5 Day / 3 hour forcast:

response = requests.get(url=Open_Weather_Map_Endpoint, params=weather_parameters)
response.raise_for_status()
weather_data = response.json()
all_day_weather = weather_data['list']

will_rain = False
time = None
for hour_data in all_day_weather:
    weather_id = hour_data['weather'][0]['id']
    time = hour_data['dt_txt']
    if weather_id < 700:  # above that weather code have nice weather.
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="{country_code}{your_number}",
        from_= os.getenv("Online_phone_number"),
        body=f"It's going to rain today at {time}. Remember to bring an ☔")
    print(message.status)

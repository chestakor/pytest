import telebot
from telebot import types
from keep_alive import keep_alive
import str1  # Import the new str1.py

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello, sir!")

@bot.message_handler(commands=['chk'])
def check_card_command(message):
    chat_id = message.chat.id
    str1.process_chk_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

import telebot
from telebot import types
from keep_alive import keep_alive
import str1  # Import str1.py for the /chk command
import seedr  # Import seedr.py for the /seedr command

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello, sir!")

@bot.message_handler(commands=['chk'])
def check_card_command(message):
    chat_id = message.chat.id
    str1.process_chk_command(bot, message)

@bot.message_handler(commands=['seedr'])
def check_seedr_command(message):
    chat_id = message.chat.id
    seedr.process_seedr_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

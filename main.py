import telebot
from keep_alive import keep_alive
import str1  # Example for /chk command
import seedr  # Example for /seedr command
import nonsk1  # Example for /nonsk1 command
import hoi  # Example for /hoi command
import crunchy
import grab
import nonsk2
import help

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

@bot.message_handler(commands=['nonsk1'])
def check_nonsk1_command(message):
    chat_id = message.chat.id
    nonsk1.process_nonsk1_command(bot, message)

@bot.message_handler(commands=['hoi'])
def check_hoi_command(message):
    chat_id = message.chat.id
    hoi.process_hoi_command(bot, message)

@bot.message_handler(commands=['crunchy'])
def check_crunchy_command(message):
    chat_id = message.chat.id
    crunchy.process_crunchy_command(bot, message)

@bot.message_handler(commands=['grab'])
def grab_command(message):
    chat_id = message.chat.id
    grab.process_grab_command(bot, message)

@bot.message_handler(commands=['nonsk2'])
def check_nonsk2_command(message):
    chat_id = message.chat.id
    nonsk2.process_nonsk2_command(bot, message)

@bot.message_handler(commands=['help'])
def help_command(message):
    help.process_help_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

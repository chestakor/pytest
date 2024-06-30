import telebot
from telebot import types
from keep_alive import keep_alive
import str1  # Example for /chk command
import seedr  # Example for /seedr command
import nonsk1  # Example for /nonsk1 command

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0', request_kwargs={
    'read_timeout': 60,  # Increase read timeout to 60 seconds
    'connect_timeout': 60,  # Increase connect timeout to 60 seconds
})

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

def start_polling_with_retries(bot, retries=5):
    for _ in range(retries):
        try:
            bot.polling()
            break
        except requests.exceptions.ReadTimeout as e:
            print(f"ReadTimeout occurred: {e}. Retrying...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying...")

if __name__ == "__main__":
    keep_alive()
    start_polling_with_retries(bot)

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
import nonsk3
from telebot import types

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    gates_text = (
        "－－－－－－－－－－－－－－－－\n"
        "            𝗪𝗘𝗟𝗖𝗢𝗠𝗘  💬\n"
        "－－－－－－－－－－－－－－－－\n"
        " •├𝗣𝗥𝗘𝗠𝗜𝗨𝗠 ➢ 8\n"
        " •├𝗦𝗧𝗔𝗡𝗗𝗔𝗥𝗗 ➢ 5\n"
        " •├𝗙𝗥𝗘𝗘 ➢ 3\n\n"
        "－－－－－－－－－－－－－－－－\n"
        " •├Dev ➣ @aftab_kabir\n"
        "－－－－－－－－－－－－－－－－"
    )
    
    welcome_text = (
        "Hello, sir!\n"
        "Use /help to know all command\n"
        "Owner: Aftab👑\n\n"
    )
    
    full_caption = welcome_text + gates_text
    
    gates_keyboard = types.InlineKeyboardMarkup(row_width=2)
    gates_keyboard.add(
        types.InlineKeyboardButton('𝗦𝗧𝗔𝗡𝗗𝗔𝗥𝗗 ✨', callback_data='premium'),
        types.InlineKeyboardButton('𝗙𝗥𝗘𝗘 🥁', callback_data='free'),
        types.InlineKeyboardButton('𝗛𝗢𝗠𝗘', callback_data='back2')
    )
    
    video_url = "https://link.anshbotzone.tech/349273/ezgif.com-gif-to-mp4-converter.mp4?hash=50dd83"
    
    bot.send_video(chat_id, video_url, caption=full_caption, parse_mode='HTML', reply_markup=gates_keyboard)

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

@bot.message_handler(commands=['nsk3'])
def handle_nsk3(message):
    nonsk3.handle_nonsk3_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

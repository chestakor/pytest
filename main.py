import telebot
from telebot import types
from keep_alive import keep_alive
import str1  # Example for /chk command
import seedr  # Example for /seedr command
import nonsk1  # Example for /nonsk1 command
import hoi  # Example for /hoi command
import crunchy
import grab
import nonsk2
import nonsk3

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')

premium_text = (
    "### [GATES]\n\n"
    "💳 STRIPE Charge - [ TEST ]\n"
    "- Format: /chk cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 02:54:04 14-02-2024\n\n"
    "💳 NONSK CHECKER-1 - [ TEST ]\n"
    "- Format: /nonsk1 cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 12:58:42 10-02-2024\n\n"
    "💳 NONSK CHECKER-2 - [ TEST ]\n"
    "- Format: /nonsk2 cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 17:40:35 20-02-2024\n\n"
    "(MORE COMING SOON)"
)

free_text = (
    "### [TOOL]\n\n"
    "🌐 Website: Seedr\n"
    "- Format: /seedr email:pass\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Website: Crunchyroll\n"
    "- Format: /crunchy email:pass\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Website: Hoichoi\n"
    "- Format: /hoi email:pass\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Website: Zee5 Global\n"
    "- Format: /z email:pass\n"
    "- Status: Coming Soon 🌦\n\n"
    "🌐 Website: Stripe CS PK GRABBER\n"
    "- Format: /grab url\n"
    "- Status: ACTIVE ✅\n"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    welcome_text = (
        "Hello, sir!\n"
        "Use /help to know all command\n"
        "Owner: Aftab👑\n\n"
    )
    gates_text = (
        "－－－－－－－－－－－－－－－－\n"
        "            WELCOME  💬\n"
        "－－－－－－－－－－－－－－－－\n"
        " •├PREMIUM ➢ 8\n"
        " •├STANDARD ➢ 5\n"
        " •├FREE ➢ 3\n\n"
        "－－－－－－－－－－－－－－－－\n"
        " •├Dev ➣ @aftab_kabir\n"
        "－－－－－－－－－－－－－－－－"
    )
    
    full_caption = welcome_text + gates_text
    
    gates_keyboard = types.InlineKeyboardMarkup(row_width=2)
    gates_keyboard.add(
        types.InlineKeyboardButton('GATE ✨', callback_data='show_gates'),
        types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'),
        types.InlineKeyboardButton('HOME', callback_data='home')
    )
    
    video_url = "https://link.anshbotzone.tech/349273/ezgif.com-gif-to-mp4-converter.mp4?hash=50dd83"
    
    bot.send_video(chat_id, video_url, caption=full_caption, reply_markup=gates_keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['show_gates', 'show_tools', 'home'])
def handle_callback_query(call):
    if call.data == 'show_gates':
        gates_keyboard = types.InlineKeyboardMarkup(row_width=2)
        gates_keyboard.add(
            types.InlineKeyboardButton('GATE ✨', callback_data='show_gates'),
            types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'),
            types.InlineKeyboardButton('HOME', callback_data='home')
        )
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=premium_text, reply_markup=gates_keyboard)
    elif call.data == 'show_tools':
        tools_keyboard = types.InlineKeyboardMarkup(row_width=2)
        tools_keyboard.add(
            types.InlineKeyboardButton('GATE ✨', callback_data='show_gates'),
            types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'),
            types.InlineKeyboardButton('HOME', callback_data='home')
        )
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=free_text, reply_markup=tools_keyboard)
    elif call.data == 'home':
        send_welcome(call.message)

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
    chat_id = message.chat.id
    gate_keyboard = types.InlineKeyboardMarkup(row_width=1)
    gate_keyboard.add(types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'))
    bot.send_message(chat_id, premium_text, reply_markup=gate_keyboard)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

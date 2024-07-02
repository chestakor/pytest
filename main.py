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

welcome_text = (
    "Hello, sir!\n"
    "Use /help to know all command\n"
    "Owner: Aftab👑\n\n"
    "－－－－－－－－－－－－－－－－\n"
    "            WELCOME 💬\n"
    "－－－－－－－－－－－－－－－－\n"
    " • PREMIUM ➢ 8\n"
    " • STANDARD ➢ 5\n"
    " • FREE ➢ 3\n\n"
    "－－－－－－－－－－－－－－－－\n"
    " • Dev ➣ @aftab_kabir\n"
    "－－－－－－－－－－－－－－－－"
)

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

gates_keyboard = types.InlineKeyboardMarkup(row_width=2)
gates_keyboard.add(
    types.InlineKeyboardButton('GATE ✨', callback_data='premium'),
    types.InlineKeyboardButton('TOOLS 🥁', callback_data='free'),
    types.InlineKeyboardButton('HOME', callback_data='home')
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    video_url = "https://link.anshbotzone.tech/349273/ezgif.com-gif-to-mp4-converter.mp4?hash=50dd83"
    bot.send_video(chat_id, video_url, caption=welcome_text, parse_mode='HTML', reply_markup=gates_keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['premium', 'free', 'home'])
def handle_callback_query(call):
    if call.data == 'premium':
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=premium_text, parse_mode='HTML', reply_markup=gates_keyboard)
    elif call.data == 'free':
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=free_text, parse_mode='HTML', reply_markup=gates_keyboard)
    elif call.data == 'home':
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=welcome_text, parse_mode='HTML', reply_markup=gates_keyboard)
        
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

@bot.callback_query_handler(func=lambda call: call.data in ['show_tools', 'show_gates'])
def handle_help_callback_query(call):
    help.handle_help_callback_query(call)

@bot.message_handler(commands=['nsk3'])
def handle_nsk3(message):
    nonsk3.handle_nonsk3_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

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
import juicy
import nonsk3
import nonsk4
from telebot import types
import clean
import weather
import nubile
import address
import gen
import bin
import sk
import hoitxt
import info
import nord
import panda
import bg
import hma
import nagad
import dork
import grizzly


bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')

welcome_text = (
    "－－－－－－－－－－－－－－－－\n"
    "              WELCOME ⚡️\n"
    "－－－－－－－－－－－－－－－－\n"
    " • GATES ➢ 3[Test]\n"
    " • TOOLS ➢ 11\n"
    "－－－－－－－－－－－－－－－－\n"
    " • Dev ➣ @aftab_kabirr\n"
    "－－－－－－－－－－－－－－－－\n"
    "I'm Jarvis!\n"
    "Use /help to know all command\n"
    "Owner: Aftab👑\n\n"
)

premium_text = (
    "### [GATES]\n\n"
    "💳 STRIPE Charge - [ TEST🧪 ]\n"
    "- Format: /chk cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 02:54:04 14-02-2024\n\n"
    "💳 NONSK CHECKER-1 - [ ON✅ ]\n"
    "- Format: /nonsk1 cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 12:58:42 10-02-2024\n\n"
    "💳 NONSK CHECKER-2 - [ TEST🧪 ]\n"
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
    "- Status: ACTIVE ✅\n\n"
    "🌐 Weather\n"
    "- Format: /weather city_name\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Address\n"
    "- Format: /address\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Clean\n"
    "- Format: /clean data\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Generate CC\n"
    "- Format: /gen bin\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Bin\n"
    "- Format: /bin bin\n"
    "- Status: ACTIVE ✅\n\n"
    "🌐 Nord VPN\n"
    "- Format: /nord email:pass\n"
    "- Status: Testing 🧪\n\n"
    "🌐 Panda VPN\n"
    "- Format: /panda email:pass\n"
    "- Status: Testing 🧪\n"
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

@bot.message_handler(commands=['panda'])
def check_panda_command(message):
    panda.process_panda_command(bot, message)

@bot.message_handler(commands=['nubile'])
def nubile_command(message):
    nubile.process_nubile_command(bot, message)

@bot.message_handler(commands=['juicy'])
def handle_juicy_command(message):
    juicy.process_juicy_command(bot, message)

@bot.message_handler(commands=['hoitxt'])
def handle_hoitxt_command(message):
    hoitxt.process_hoitxt_command(bot, message)

# Handler for document upload
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    hoitxt.handle_docs(bot, message)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    hoitxt.handle_callback_query(call, bot)

@bot.message_handler(commands=['nagad'])
def nagad_command(message):
    nagad.process_nagad_command(bot, message)

@bot.message_handler(commands=['nonsk4'])
def handle_nonsk4_command(message):
    import nonsk4
    nonsk4.handle_nonsk4_command(bot, message)

@bot.message_handler(commands=['grizzly'])
def handle_grizzly_command(message):
    grizzly.process_grizzly_command(bot, message)

@bot.message_handler(commands=['bin'])
def bin_command(message):
    bin.process_bin_command(bot, message)
    
@bot.message_handler(commands=['bg'])
def check_bg_command(message):
    chat_id = message.chat.id
    bg.process_bg_command(bot, message)

@bot.message_handler(commands=['dork'])
def handle_dork_command(message):
    dork.process_dork_command(bot, message)

@bot.message_handler(commands=['nord'])
def nord_command(message):
    nord.process_nord_command(bot, message)

@bot.message_handler(commands=['gen'])
def generate_cc_command(message):
    gen.process_gen_command(bot, message)

@bot.message_handler(commands=['sk'])
def handle_sk(message):
    sk.process_sk_command(bot, message)

@bot.message_handler(commands=['info'])
def handle_info(message):
    info.process_info_command(bot, message)

@bot.message_handler(commands=['address'])
def address_command(message):
    address.process_address_command(bot, message)

@bot.message_handler(commands=['weather'])
def check_weather_command(message):
    chat_id = message.chat.id
    weather.process_weather_command(bot, message)

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
def handle_nonsk2_command(message):
    nonsk2.process_nonsk2_command(bot, message)

# Handler for document upload
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    nonsk2.handle_docs(bot, message)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    nonsk2.handle_callback_query(call, bot)

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    gate_text = (
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

    tool_keyboard = types.InlineKeyboardMarkup(row_width=1)
    tool_keyboard.add(types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'))
    bot.send_message(chat_id, gate_text, reply_markup=tool_keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['show_tools', 'show_gates'])
def handle_help_callback(call):
    if call.data == 'show_tools':
        tool_text = (
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
        gate_keyboard = types.InlineKeyboardMarkup(row_width=1)
        gate_keyboard.add(types.InlineKeyboardButton('GATE ✨', callback_data='show_gates'))
        bot.edit_message_text(tool_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=gate_keyboard)
    elif call.data == 'show_gates':
        gate_text = (
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
        tool_keyboard = types.InlineKeyboardMarkup(row_width=1)
        tool_keyboard.add(types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'))
        bot.edit_message_text(gate_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=tool_keyboard)

@bot.message_handler(commands=['nonsk3'])
def handle_nonsk3_command(message):
    nonsk3.handle_nonsk3_command(bot, message)
    
@bot.message_handler(commands=['clean'])
def clean_command(message):
    clean.process_clean_command(bot, message)

if __name__ == "__main__":
    keep_alive()
    bot.polling()

from telebot import types

from main import bot

# Define the gate and tool texts
gate_text = (
    "### [GATES]\n\n"
    "💳 STRIPE Charge - [ TEST🧪 ]\n"
    "- Format: /chk cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 02:54:04 14-02-2024\n\n"
    "💳 NONSK CHECKER-1 - [ TEST✅ ]\n"
    "- Format: /nonsk1 cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 12:58:42 10-02-2024\n\n"
    "💳 NONSK CHECKER-2 - [ TEST🧪 ]\n"
    "- Format: /nonsk2 cc|mon|year|cvv\n"
    "- Gateway: Stripe » FREE\n"
    "- Updated: 17:40:35 20-02-2024\n\n"
    "(MORE COMING SOON)"
)

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

def process_help_command(bot, message):
    chat_id = message.chat.id
    gate_keyboard = types.InlineKeyboardMarkup(row_width=1)
    gate_keyboard.add(types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'))
    
    bot.send_message(chat_id, gate_text, reply_markup=gate_keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['show_tools', 'show_gates'])
def handle_help_callback_query(call):
    if call.data == 'show_tools':
        tool_keyboard = types.InlineKeyboardMarkup(row_width=1)
        tool_keyboard.add(types.InlineKeyboardButton('GATES ✨', callback_data='show_gates'))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=tool_text, reply_markup=tool_keyboard)
    elif call.data == 'show_gates':
        gate_keyboard = types.InlineKeyboardMarkup(row_width=1)
        gate_keyboard.add(types.InlineKeyboardButton('TOOLS 🥁', callback_data='show_tools'))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=gate_text, reply_markup=gate_keyboard)

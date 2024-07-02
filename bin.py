import requests
from telebot import types
import time

def get_bin_info(bin_number):
    try:
        url = f"https://lookup.binlist.net/{bin_number}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        info = {
            "scheme": data.get("scheme", "N/A"),
            "type": data.get("type", "N/A"),
            "brand": data.get("brand", "N/A"),
            "country": data.get("country", {}).get("name", "N/A"),
            "bank": data.get("bank", {}).get("name", "N/A"),
            "country_code": data.get("country", {}).get("alpha2", "N/A")
        }
        return info
    except requests.exceptions.RequestException as e:
        return None

def process_bin_command(bot, message):
    chat_id = message.chat.id
    text = message.text.split()[1:]  # Get the bin number from the command
    if text:
        bin_number = text[0]
        info = get_bin_info(bin_number)
        if info:
            response_text = (
                f"↯ BIN INFORMATION\n\n"
                f"𝗕𝗜𝗡: {bin_number}\n"
                f"𝗦𝗰𝗵𝗲𝗺𝗲: {info['scheme']}\n"
                f"𝗧𝘆𝗽𝗲: {info['type']}\n"
                f"𝗕𝗿𝗮𝗻𝗱: {info['brand']}\n"
                f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {info['country']} ({info['country_code']})\n"
                f"𝗕𝗮𝗻𝗸: {info['bank']}\n\n"
                f"－－－－－－－－－－－－－－－－\n"
                f"⚫️ Total BIN fetched - 1\n"
                f"⏱️ Time Taken - 0.02 seconds\n"
                f"▫️ Checked by: {message.from_user.username}\n"
                f"⚡️ Bot by - AFTAB 👑\n"
                f"－－－－－－－－－－－－－－－－"
            )
        else:
            response_text = (
                f"Could not retrieve BIN information for {bin_number}. "
                f"Please check the BIN number and try again."
            )
    else:
        response_text = "Please provide a BIN number in the format: /bin 123456"

    bot.send_message(chat_id, response_text)

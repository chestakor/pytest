import requests
import json
import time

def process_bin_command(bot, message):
    chat_id = message.chat.id
    text = message.text.split(maxsplit=1)
    
    if len(text) < 2:
        bot.send_message(chat_id, "Please provide a valid BIN ")
        return
    
    input_value = text[1]
    bin_number = input_value[:6]  # Extract the first 6 digits for the BIN
    
    start_time = time.time()
    result = get_bin_info(bin_number)
    elapsed_time = time.time() - start_time
    response_message = format_response(result, bin_number, elapsed_time, message.from_user.username)
    bot.send_message(chat_id, response_message)

def get_bin_info(bin_number):
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin_number}')
        response_data = response.json()
        
        return {
            'scheme': response_data.get('scheme', 'Unknown').upper(),
            'type': response_data.get('type', 'Unknown').upper(),
            'brand': response_data.get('brand', 'Unknown').upper(),
            'bank': response_data.get('bank', {}).get('name', 'Unknown').upper(),
            'country': response_data.get('country', {}).get('name', 'Unknown').upper()
        }
    except Exception as e:
        return str(e)

def format_response(data, bin_number, elapsed_time, username):
    if isinstance(data, str):
        return data
    
    return (f"↯ BIN INFORMATION\n\n"
            f"BIN: {bin_number}\n"
            f"Brand: {data['brand']}\n"
            f"Type: {data['type']}\n"
            f"Scheme: {data['scheme']}\n"
            f"Bank: {data['bank']}\n"
            f"Country: {data['country']}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－")

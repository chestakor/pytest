import random
from datetime import datetime
import requests

def luhn_algorithm(cc_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(cc_number)
    checksum = 0
    reverse_digits = digits[::-1]
    for i, digit in enumerate(reverse_digits):
        if i % 2 == 0:
            doubled = digit * 2
            if doubled > 9:
                doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    return checksum % 10 == 0

def generate_cc(bin_str, mm=None, yy=None, cvc=None, amount=10):
    generated_cards = []
    for _ in range(amount):
        while True:
            cc_number = bin_str + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_str) - 1)])
            if luhn_algorithm(cc_number):
                break
        exp_month = mm if mm else str(random.randint(1, 12)).zfill(2)
        exp_year = yy if yy else str(random.randint(datetime.now().year % 100, datetime.now().year % 100 + 10)).zfill(2)
        cvc_code = cvc if cvc else str(random.randint(100, 999)).zfill(3)
        generated_cards.append(f"{cc_number}|{exp_month}|20{exp_year}|{cvc_code}")
    return generated_cards

def get_bin_info(bin_str):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_str}")
        if response.status_code == 200:
            data = response.json()
            return {
                "scheme": data.get("scheme", "N/A"),
                "type": data.get("type", "N/A"),
                "brand": data.get("brand", "N/A"),
                "bank": data.get("bank", {}).get("name", "N/A"),
                "country": data.get("country", {}).get("name", "N/A"),
                "emoji": data.get("country", {}).get("emoji", "")
            }
        else:
            return None
    except Exception as e:
        return None

def process_gen_command(bot, message):
    chat_id = message.chat.id
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.send_message(chat_id, "Please provide a valid BIN.")
        return
    
    bin_str = command_parts[1]
    mm, yy, cvc, amount = None, None, None, 10
    
    if len(command_parts) > 2:
        date_parts = command_parts[2].split('|')
        if len(date_parts) == 2:
            mm, yy = date_parts[0], date_parts[1]
        elif len(date_parts) == 3:
            mm, yy, cvc = date_parts[0], date_parts[1], date_parts[2]
    
    if len(command_parts) == 4:
        try:
            amount = int(command_parts[3])
        except ValueError:
            bot.send_message(chat_id, "Please provide a valid amount.")
            return
    
    generated_cards = generate_cc(bin_str, mm, yy, cvc, amount)
    bin_info = get_bin_info(bin_str)
    
    response_text = f"↯ CC GENERATOR\n\nBIN ➔ {bin_str}\nAmount ➔ {amount}\n\n"
    response_text += "\n".join(generated_cards) + "\n\n"
    
    if bin_info:
        response_text += (
            f"Info: {bin_info['scheme'].upper()} - {bin_info['type'].upper()} - {bin_info['brand'].upper()}\n"
            f"Issuer: {bin_info['bank']}\n"
            f"Country: {bin_info['country']} {bin_info['emoji']}\n\n"
        )
    
    response_text += (
        "－－－－－－－－－－－－－－－－\n"
        f"⚫️ Total CC Generated - {amount}\n"
        f"⏱️ Time Taken - {round(time.time() - start_time, 2)} seconds\n"
        f"▫️ Checked by: {message.from_user.username}\n"
        "⚡️ Bot by - AFTAB 👑\n"
        "－－－－－－－－－－－－－－－－"
    )
    
    bot.send_message(chat_id, response_text)

# In your main.py, import and use this function
# from gen import process_gen_command

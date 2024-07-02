import random
import datetime
import requests
import time

def luhn_residue(digits):
    return sum(sum(divmod(int(d) * (1 + i % 2), 10))
               for i, d in enumerate(digits[::-1])) % 10

def generate_cc(bin, month, year, cvc, amount):
    results = []
    for _ in range(amount):
        cc_number = bin
        while len(cc_number) < 15:
            cc_number += str(random.randint(0, 9))
        cc_number += str((10 - luhn_residue(cc_number)) % 10)
        cvc_code = cvc if cvc != "xxx" else str(random.randint(100, 999))
        results.append(f"{cc_number}|{month}|{year}|{cvc_code}")
    return results

def get_bin_info(bin):
    url = f"https://lookup.binlist.net/{bin}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        info = {
            "brand": data.get("scheme", "N/A").upper(),
            "type": data.get("type", "N/A").upper(),
            "level": data.get("brand", "N/A").upper(),
            "issuer": data.get("bank", {}).get("name", "N/A"),
            "country": data.get("country", {}).get("name", "N/A"),
            "country_code": data.get("country", {}).get("alpha2", "N/A")
        }
        return info
    return None

def process_gen_command(bot, message):
    start_time = time.time()
    try:
        chat_id = message.chat.id
        input_data = message.text.split()[1]
        if '|' in input_data:
            bin_part, month, year = input_data.split('|')
            cvc = 'xxx'
            amount = 10
        else:
            parts = input_data.split()
            bin_part = parts[0]
            month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
            year = parts[2] if len(parts) > 2 else str(random.randint(datetime.datetime.now().year, datetime.datetime.now().year + 5))[2:]
            cvc = parts[3] if len(parts) > 3 else 'xxx'
            amount = int(parts[4]) if len(parts) > 4 else 10

        cc_list = generate_cc(bin_part, month, year, cvc, amount)
        bin_info = get_bin_info(bin_part[:6])
        
        response_text = f"𝗕𝗜𝗡 ⇾ {bin_part[:6]}\n𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ {amount}\n\n"
        response_text += "\n".join(cc_list) + "\n\n"
        if bin_info:
            response_text += f"𝗜𝗻𝗳𝗼: {bin_info['brand']} - {bin_info['type']} - {bin_info['level']}\n"
            response_text += f"𝐈𝐬𝐬𝐮𝐞𝐫: {bin_info['issuer']}\n"
            response_text += f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country']} 🇿🇦\n"

        elapsed_time = time.time() - start_time
        response_text += (
            f"－－－－－－－－－－－－－－－－\n"
            f"⚫️ Total CC Generated - {amount}\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

        bot.send_message(chat_id, response_text, parse_mode='HTML')
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

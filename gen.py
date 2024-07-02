import time
import random
import requests

def luhn_algorithm(cc_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(cc_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def generate_random_cvc():
    return str(random.randint(100, 999))

def generate_random_exp_date():
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(24, 32))
    return month, year

def generate_cc(bin_info, mm=None, yy=None, cvc=None, amount=10):
    generated_ccs = []
    for _ in range(amount):
        cc_number = bin_info + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_info) - 1)])
        checksum_digit = [str(digit) for digit in range(10) if luhn_algorithm(cc_number + str(digit))][0]
        cc_number += checksum_digit

        if not mm or not yy:
            mm, yy = generate_random_exp_date()
        if not cvc:
            cvc = generate_random_cvc()

        generated_ccs.append(f"{cc_number}|{mm}|{yy}|{cvc}")

    return "\n".join(generated_ccs)

def fetch_bin_info(bin_info):
    response = requests.get(f'https://lookup.binlist.net/{bin_info}')
    if response.status_code == 200:
        return response.json()
    return {}

def process_gen_command(bot, message):
    chat_id = message.chat.id
    text = message.text.split()
    
    # Parsing user input
    if len(text) < 2:
        bot.send_message(chat_id, "Please provide a BIN.")
        return

    bin_info = text[1]
    try:
        mm = text[2]
        yy = text[3]
        cvc = text[4]
        amount = int(text[5]) if len(text) > 5 else 10
    except IndexError:
        mm, yy, cvc = None, None, None
        amount = int(text[2]) if len(text) > 2 else 10

    start_time = time.time()  # Define start_time here

    generated_cc = generate_cc(bin_info, mm, yy, cvc, amount)
    bin_details = fetch_bin_info(bin_info)

    name = bin_details.get('country', {}).get('name', '').upper()
    brand = bin_details.get('scheme', '').upper()
    type_ = bin_details.get('type', '').upper()
    bank = bin_details.get('bank', {}).get('name', '').upper()

    result_text = (
        f"𝗕𝗜𝗡 ⇾ {bin_info}\n"
        f"𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ {amount}\n\n"
        f"{generated_cc}\n\n"
        f"𝗜𝗻𝗳𝗼: {brand} - {type_}\n"
        f"𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n"
        f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {name}\n\n"
        f"－－－－－－－－－－－－－－－－\n"
        f"⏱️ Time Taken - {round(time.time() - start_time, 2)} seconds\n"
        f"▫️ Checked by: {message.from_user.username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    
    bot.send_message(chat_id, result_text, parse_mode='HTML')

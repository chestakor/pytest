import requests
import time

def process_chk_command(bot, message):
    chat_id = message.chat.id
    card_data = message.text.split()[1:]  # Get the card data from the command
    if card_data:
        total_cards = len(card_data)
        start_time = time.time()
        results = []
        initial_message = "↯ STRIPE CHARGE 1$\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in card_data:
            result = check_card_details(card)
            results.append(f"{card}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide card details in the format: /chk cc|mm|yy|cvc")

def check_card_details(card):
    try:
        card_parts = card.split('|')
        if len(card_parts) != 4:
            return "Invalid card format"

        cc, mes, ano, cvv = card_parts
        if len(mes) == 1:
            mes = "0" + mes
        if len(ano) == 2:
            ano = "20" + ano

        # Replace this with your actual secret key
        sk = "YOUR_SECRET_KEY"

        # 1st Request
        api_url_1 = "https://api.stripe.com/v1/payment_methods"
        headers = {
            "Authorization": f"Bearer {sk}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data_1 = {
            "type": "card",
            "card[number]": cc,
            "card[exp_month]": mes,
            "card[exp_year]": ano,
            "card[cvc]": cvv
        }
        response_1 = requests.post(api_url_1, headers=headers, data=data_1)
        result_1 = response_1.json()

        if "rate_limit" in response_1.text:
            return "Rate limit exceeded, please try again later."

        tok1 = result_1.get("id")

        if not tok1:
            return "Failed to get token for card"

        # 2nd Request
        api_url_2 = "https://api.stripe.com/v1/payment_intents"
        data_2 = {
            "amount": 100,  # Amount in cents
            "currency": "usd",
            "payment_method_types[]": "card",
            "description": "Custom Donation",
            "payment_method": tok1
        }
        response_2 = requests.post(api_url_2, headers=headers, data=data_2)
        result_2 = response_2.json()

        if "rate_limit" in response_2.text:
            return "Rate limit exceeded, please try again later."

        pi_id = result_2.get("id")

        if not pi_id:
            return "Failed to create PaymentIntent"

        # 3rd Request
        api_url_3 = f"https://api.stripe.com/v1/payment_intents/{pi_id}/confirm"
        response_3 = requests.post(api_url_3, headers=headers)
        result_3 = response_3.json()

        if "rate_limit" in response_3.text:
            return "Rate limit exceeded, please try again later."

        if "seller_message" in result_3 and result_3["seller_message"] == "Payment complete.":
            return "CHARGED $1 ✅"
        elif "cvc_check" in result_3 and result_3["cvc_check"] == "pass":
            return "CVV LIVE ✅"
        elif "cvc_check" in result_3 and result_3["cvc_check"] == "fail":
            return "Security code is incorrect 🚫"
        elif "generic_decline" in result_3 or "generic_decline" in response_1.text:
            return "GENERIC DECLINED 🚫"
        elif "insufficient_funds" in result_3:
            return "INSUFFICIENT FUNDS 🚫"
        elif "fraudulent" in result_3:
            return "FRAUDULENT 🚫"
        elif "do_not_honor" in result_3 or "do_not_honor" in response_1.text:
            return "DO NOT HONOR 🚫"
        elif "incorrect_cvc" in result_3 or "invalid_cvc" in response_1.text:
            return "Security code is incorrect 🚫"
        elif "invalid_expiry_month" in response_1.text:
            return "INVALID EXPIRY MONTH 🚫"
        elif "invalid_account" in result_3:
            return "INVALID ACCOUNT 🚫"
        elif "lost_card" in result_3:
            return "LOST CARD 🚫"
        elif "stolen_card" in result_3:
            return "STOLEN CARD 🚫"
        elif "transaction_not_allowed" in result_3:
            return "TRANSACTION NOT ALLOWED 🚫"
        elif "authentication_required" in result_3 or "card_error_authentication_required" in response_1.text:
            return "3DS REQUIRED 🚫"
        elif "pickup_card" in result_3:
            return "PICKUP CARD 🚫"
        elif "Your card has expired." in result_3:
            return "EXPIRED CARD 🚫"
        elif "card_decline_rate_limit_exceeded" in result_3:
            return "SK IS AT RATE LIMIT 🚫"
        elif "processing_error" in result_3:
            return "PROCESSING ERROR 🚫"
        elif "Your card number is incorrect." in result_3 or "incorrect_number" in response_1.text:
            return "Incorrect Card Number 🚫"
        elif "service_not_allowed" in result_3:
            return "SERVICE NOT ALLOWED 🚫"
        elif "card_not_supported" in result_3:
            return "CARD NOT SUPPORTED 🚫"
        elif "testmode_charges_only" in response_1.text:
            return "SK KEY DEAD OR INVALID 🚫"
        elif "api_key_expired" in response_1.text:
            return "SK KEY REVOKED 🚫"
        elif "parameter_invalid_empty" in response_1.text:
            return "ENTER CC TO CHECK 🚫"

        return f"DEAD: {result_3.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        print(f"An error occurred in check_card_details: {str(e)}")  # Log error for debugging
        return f"An error occurred while checking the card: {str(e)}"

def get_footer_info(total_cards, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"[ CHECK INFO ]\n"
        f"⌧ Total CC Checked - {total_cards}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer


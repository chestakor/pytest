import telebot
from telebot import types
import requests
import json
import time
from keep_alive import keep_alive

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0')
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello, sir!")

@bot.message_handler(commands=['chk'])
def check_card_command(message):
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
        sk = "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"

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

        # 2nd Request
        api_url_2 = "https://api.stripe.com/v1/payment_intents"
        data_2 = {
            "amount": 100,  # Amount in cents
            "currency": "usd",
            "payment_method_types[]": "card",
            "description": "Custom Donation",
            "payment_method": tok1,
            "confirm": "true",
            "off_session": "true"
        }
        response_2 = requests.post(api_url_2, headers=headers, data=data_2)
        result_2 = response_2.json()

        if "rate_limit" in response_2.text:
            return "Rate limit exceeded, please try again later."

        if "seller_message" in result_2 and result_2["seller_message"] == "Payment complete.":
            return "CHARGED $1 ✅"
        elif "cvc_check" in result_2 and result_2["cvc_check"] == "pass":
            return "CVV LIVE ✅"
        elif "cvc_check" in result_2 and result_2["cvc_check"] == "fail":
            return "Security code is incorrect 🚫"
        elif "generic_decline" in result_2 or "generic_decline" in response_1.text:
            return "GENERIC DECLINED 🚫"
        elif "insufficient_funds" in result_2:
            return "INSUFFICIENT FUNDS 🚫"
        elif "fraudulent" in result_2:
            return "FRAUDULENT 🚫"
        elif "do_not_honor" in result_2 or "do_not_honor" in response_1.text:
            return "DO NOT HONOR 🚫"
        elif "incorrect_cvc" in result_2 or "invalid_cvc" in response_1.text:
            return "Security code is incorrect 🚫"
        elif "invalid_expiry_month" in response_1.text:
            return "INVALID EXPIRY MONTH 🚫"
        elif "invalid_account" in result_2:
            return "INVALID ACCOUNT 🚫"
        elif "lost_card" in result_2:
            return "LOST CARD 🚫"
        elif "stolen_card" in result_2:
            return "STOLEN CARD 🚫"
        elif "transaction_not_allowed" in result_2:
            return "TRANSACTION NOT ALLOWED 🚫"
        elif "authentication_required" in result_2 or "card_error_authentication_required" in response_1.text:
            return "3DS REQUIRED 🚫"
        elif "pickup_card" in result_2:
            return "PICKUP CARD 🚫"
        elif "Your card has expired." in result_2:
            return "EXPIRED CARD 🚫"
        elif "card_decline_rate_limit_exceeded" in result_2:
            return "SK IS AT RATE LIMIT 🚫"
        elif "processing_error" in result_2:
            return "PROCESSING ERROR 🚫"
        elif "Your card number is incorrect." in result_2 or "incorrect_number" in response_1.text:
            return "Incorrect Card Number 🚫"
        elif "service_not_allowed" in result_2:
            return "SERVICE NOT ALLOWED 🚫"
        elif "card_not_supported" in result_2:
            return "CARD NOT SUPPORTED 🚫"
        elif "testmode_charges_only" in response_1.text:
            return "SK KEY DEAD OR INVALID 🚫"
        elif "api_key_expired" in response_1.text:
            return "SK KEY REVOKED 🚫"
        elif "parameter_invalid_empty" in response_1.text:
            return "ENTER CC TO CHECK 🚫"

        return f"DEAD: {result_2.get('error', {}).get('message', 'Unknown error')}"
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

if __name__ == "__main__":
    keep_alive()
    bot.polling()

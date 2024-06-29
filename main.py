import telebot
from telebot import types
import requests
import json
from keep_alive import keep_alive

bot = telebot.TeleBot('7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0') # Replace 'Bot Token' with your actual bot token
user_states = {}

# Delete webhook if it exists


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Hello, sir!")

@bot.message_handler(commands=['chk'])
def check_card_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = {"state": "awaiting_card_details"}
    bot.send_message(chat_id, "Please enter your card details in the format: cc|mm|yy|cvc")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)

    if user_data and user_data["state"] == "awaiting_card_details":
        card_details = message.text
        result = check_card_details(card_details)
        bot.send_message(chat_id, result)
        user_states.pop(chat_id, None)
    else:
        bot.send_message(chat_id, "Unknown command or state. Please start over.")

def check_card_details(card):
    try:
        card_parts = card.split('|')
        if len(card_parts) != 4:
            return f"Invalid card format: {card}"

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

        print(f"Response 1: {response_1.text}")  # Log response

        if "rate_limit" in response_1.text:
            return "Rate limit exceeded, please try again later."

        tok1 = result_1.get("id")
        if not tok1:
            return f"Failed to get token for card: {card}"

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

        print(f"Response 2: {response_2.text}")  # Log response

        if "rate_limit" in response_2.text:
            return "Rate limit exceeded, please try again later."

        if "seller_message" in result_2 and result_2["seller_message"] == "Payment complete.":
            receipt_url = result_2.get("receipt_url", "No receipt URL")
            return f"CHARGED: {card}\nResponse: $1 Charged ✅\nReceipt: {receipt_url}"
        elif "cvc_check" in result_2 and result_2["cvc_check"] == "pass":
            return f"CVV LIVE: {card}"
        elif "cvc_check" in result_2 and result_2["cvc_check"] == "fail":
            return f"Security code is incorrect: {card}"
        elif "generic_decline" in result_2 or "generic_decline" in response_1.text:
            return f"DEAD: {card}\nResult: GENERIC DECLINED"
        elif "insufficient_funds" in result_2:
            return f"CVV: {card}\nResult: INSUFFICIENT FUNDS"
        elif "fraudulent" in result_2:
            return f"DEAD: {card}\nResult: FRAUDULENT"
        elif "do_not_honor" in result_2 or "do_not_honor" in response_1.text:
            return f"DEAD: {card}\nResult: DO NOT HONOR"
        elif "incorrect_cvc" in result_2 or "invalid_cvc" in response_1.text:
            return f"CCN: {card}\nResult: Security code is incorrect"
        elif "invalid_expiry_month" in response_1.text:
            return f"DEAD: {card}\nResult: INVALID EXPIRY MONTH"
        elif "invalid_account" in result_2:
            return f"DEAD: {card}\nResult: INVALID ACCOUNT"
        elif "lost_card" in result_2:
            return f"DEAD: {card}\nResult: LOST CARD"
        elif "stolen_card" in result_2:
            return f"DEAD: {card}\nResult: STOLEN CARD"
        elif "transaction_not_allowed" in result_2:
            return f"CVV: {card}\nResult: TRANSACTION NOT ALLOWED"
        elif "authentication_required" in result_2 or "card_error_authentication_required" in response_1.text:
            return f"CVV: {card}\nResult: 3DS REQUIRED"
        elif "pickup_card" in result_2:
            return f"DEAD: {card}\nResult: PICKUP CARD"
        elif "Your card has expired." in result_2:
            return f"DEAD: {card}\nResult: EXPIRED CARD"
        elif "card_decline_rate_limit_exceeded" in result_2:
            return f"DEAD: {card}\nResult: SK IS AT RATE LIMIT"
        elif "processing_error" in result_2:
            return f"DEAD: {card}\nResult: PROCESSING ERROR"
        elif "Your card number is incorrect." in result_2 or "incorrect_number" in response_1.text:
            return f"DEAD: {card}\nResult: YOUR CARD NUMBER IS INCORRECT"
        elif "service_not_allowed" in result_2:
            return f"DEAD: {card}\nResult: SERVICE NOT ALLOWED"
        elif "card_not_supported" in result_2:
            return f"DEAD: {card}\nResult: CARD NOT SUPPORTED"
        elif "testmode_charges_only" in response_1.text:
            return f"DEAD: {card}\nResult: SK KEY DEAD OR INVALID"
        elif "api_key_expired" in response_1.text:
            return f"DEAD: {card}\nResult: SK KEY REVOKED"
        elif "parameter_invalid_empty" in response_1.text:
            return f"DEAD: {card}\nResult: ENTER CC TO CHECK"

        return f"DEAD: {card}\nResult: {response_2.text}"
    except Exception as e:
        print(f"An error occurred in check_card_details: {str(e)}")  # Log error for debugging
        return f"An error occurred while checking the card: {str(e)}"

if __name__ == "__main__":
    keep_alive()
    bot.polling()

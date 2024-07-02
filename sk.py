import requests
import time

def process_sk_command(bot, message):
    chat_id = message.chat.id
    user = message.from_user.username
    parts = message.text.split()

    if len(parts) < 2:
        response_message = (
            f"↯ SK KEY CHECK 🌟\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• No SK key provided ❌\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• Dev: @aftab_kabir\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - 0.00 seconds\n"
            f"▫️ Checked by: {user}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )
        bot.send_message(chat_id, response_message, parse_mode='HTML')
        return

    sk_key = parts[1]
    start_time = time.time()

    # First request to check the validity of the SK key
    headers = {
        'Authorization': f'Bearer {sk_key}',
    }

    data = {
        'type': 'card',
        'card[number]': '4102770015058552',
        'card[exp_month]': '06',
        'card[exp_year]': '24',
        'card[cvc]': '997',
    }

    response_1 = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
    result_1 = response_1.json()

    if 'error' not in result_1:
        # Second request to fetch balance
        response_2 = requests.get('https://api.stripe.com/v1/balance', headers=headers)
        result_2 = response_2.json()

        balance = result_2.get('available', [{'amount': '0'}])[0]['amount']
        pending_balance = result_2.get('pending', [{'amount': '0'}])[0]['amount']
        currency = result_2.get('currency', 'unknown').upper()

        response_message = (
            f"↯ SK KEY CHECK 🌟\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• LIVE SK ✅\n\n"
            f"• KEY: <code>{sk_key}</code>\n\n"
            f"• BALANCE: {balance}\n"
            f"• PENDING: {pending_balance}\n"
            f"• CURRENCY: {currency}\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• Dev: @aftab_kabir\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {round(time.time() - start_time, 2)} seconds\n"
            f"▫️ Checked by: {user}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )
    else:
        error_message = result_1['error'].get('message', 'Unknown error')
        response_message = (
            f"↯ SK KEY CHECK 🌟\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• DEAD KEY ❌\n\n"
            f"• KEY: <code>{sk_key}</code>\n\n"
            f"• STATUS: {error_message}\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• Dev: @aftab_kabir\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {round(time.time() - start_time, 2)} seconds\n"
            f"▫️ Checked by: {user}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

    bot.send_message(chat_id, response_message, parse_mode='HTML')

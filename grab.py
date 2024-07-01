import requests
from urllib.parse import unquote
import base64
import time

def process_grab_command(bot, message):
    chat_id = message.chat.id
    url = message.text.split()[1]  # Get the URL from the command
    if url:
        start_time = time.time()
        result = grab_details(url)
        elapsed_time = time.time() - start_time
        response_message = format_response(result, url, elapsed_time, message.from_user.username)
        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(chat_id, "Please provide a URL in the format: /grab url")

def grab_details(checkout):
    try:
        url = checkout.split('#')[1]
        cs = get_str(checkout, 'pay/', '#')
        pk = get_str(xor_string(base64.b64decode(unquote(url)), 5), '"apiKey":"', '"')
        site = get_str(xor_string(base64.b64decode(unquote(url)), 5), '"referrerOrigin":"', '"')

        headers = {
            'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; M1901F7S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        response = requests.post(
            f'https://api.stripe.com/v1/payment_pages/{cs}/init',
            headers=headers,
            auth=(pk, ''),
            data={'key': pk, 'eid': 'NA', 'browser_locale': 'en-US', 'redirect_type': 'stripe_js'}
        )

        if 'No such payment_page' in response.text:
            return "Expired Link"
        
        response_data = response.json()
        name = response_data.get('display_name', '____')
        email = response_data.get('customer_email', 'Email not found')
        cur = response_data.get('currency', '____')
        amt = response_data.get('amount', response_data.get('total', '____'))
        
        return {
            'name': name,
            'pklive': pk,
            'cslive': cs,
            'amount': amt,
            'email': email
        }
    except Exception as e:
        return str(e)

def get_str(string, start, end):
    str_ = string.split(start)
    str_ = str_[1].split(end)
    return str_[0]

def xor_string(text, key):
    if isinstance(key, int):
        key = [key]
    output = ''
    for i in range(len(text)):
        c = text[i]
        k = key[i % len(key)]
        output += chr(c ^ k)
    return output

def format_response(data, url, elapsed_time, username):
    if isinstance(data, str):
        return data
    return (f"↯ CS PK GRABBER\n\n"
            f"Result:\n"
            f"Name: {data['name']}\n"
            f"PK Live: {data['pklive']}\n"
            f"CS Live: {data['cslive']}\n"
            f"Amount: {data['amount']}\n"
            f"Email: {data['email']}\n\n"
            f"－－－－－－－－－－－－－－－－\n"
            f"🔹 Total URL Checked - 1\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {username}\n"
            f"⚡️ Bot by - AFTAB [BOSS]\n"
            f"－－－－－－－－－－－－－－－－")

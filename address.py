import requests
from bs4 import BeautifulSoup
import time

def get_str(source, start_str, end_str):
    start = source.find(start_str) + len(start_str)
    end = source.find(end_str, start)
    return source[start:end].strip()

def process_address_command(bot, message):
    chat_id = message.chat.id
    url = 'https://www.fakexy.com/fake-address-generator-uk'
    
    headers = {
        'Host': 'www.fakexy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv=103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers'
    }
    
    start_time = time.time()
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    street_uk = get_str(str(soup), '<td>Street</td>', '\n')
    city_uk = get_str(str(soup), '<td>City/Town</td>', '\n')
    state_uk = get_str(str(soup), '<td>State/Province/Region</td>', '\n')
    postal_uk = get_str(str(soup), '<td>Zip/Postal Code</td>', '\n')
    phone_uk = get_str(str(soup), '<td>Phone Number</td>', '\n')
    country_uk = get_str(str(soup), '<td>Country</td>', '\n')
    lat_uk = get_str(str(soup), '<td>Latitude</td>', '\n')
    lon_uk = get_str(str(soup), '<td>Longitude</td>', '\n')

    address = (
        f"Street: {street_uk}\n"
        f"City: {city_uk}\n"
        f"State: {state_uk}\n"
        f"Postal Code: {postal_uk}\n"
        f"Phone: {phone_uk}\n"
        f"Country: {country_uk}\n"
        f"Latitude: {lat_uk}\n"
        f"Longitude: {lon_uk}"
    )
    
    elapsed_time = time.time() - start_time
    result = (
        f"↯ ADDRESS INFORMATION\n\n{address}\n\n"
        f"－－－－－－－－－－－－－－－－\n"
        f"⚫️ Total address fetched - 1\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {message.from_user.username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )

    bot.send_message(chat_id, result)

import requests
from bs4 import BeautifulSoup
import random
import time

def process_dork_command(bot, message):
    chat_id = message.chat.id
    args = message.text.split(' ', 1)
    if len(args) != 2:
        bot.send_message(chat_id, "Please provide a dork query in the format: /dork query")
        return

    query = args[1]
    start_time = time.time()

    urls = search_google_dork(query)
    elapsed_time = time.time() - start_time

    if urls:
        response = format_response(urls, elapsed_time, message.from_user.username)
        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, "No results found for the given dork query.")

def search_google_dork(query):
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
    ]
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        urls = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('http')]
        filtered_urls = [url for url in urls if not url.startswith('https://www.google.') and not url.startswith('https://support.google.com')]
        return filtered_urls[:20]  # Return the first 20 results
    else:
        return []

def format_response(urls, elapsed_time, username):
    urls_text = '\n'.join(urls)
    return (
        f"🔍 Google Dork Results\n\n"
        f"{urls_text}\n\n"
        f"－－－－－－－－－－－－－－－－\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )

import requests
import re
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/18.18363",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def process_dork_command(bot, message):
    chat_id = message.chat.id
    query = ' '.join(message.text.split()[1:])
    start_time = time.time()

    if not query:
        bot.send_message(chat_id, "Please provide a dork query in the format: /dork query")
        return

    bot.send_message(chat_id, f"Searching for dork: {query}")
    try:
        urls = search_google_dork(query)
        if urls:
            response = "\n".join(urls[:20])  # Show first 20 results
            footer = get_footer_info(len(urls), start_time, message.from_user.username)
            bot.send_message(chat_id, response + "\n\n" + footer)
        else:
            bot.send_message(chat_id, "No results found for the given dork query.")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred while processing the dork query: {str(e)}")

def search_google_dork(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': get_random_user_agent()}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)
    urls = [link.get('href') for link in links if link.get('href') and link.get('href').startswith('http')]

    # Filter out Google URLs
    urls = [url for url in urls if "google.com" not in urlparse(url).netloc]

    return urls

def get_footer_info(total_urls, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"🔹 Total URLs Found - {total_urls}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

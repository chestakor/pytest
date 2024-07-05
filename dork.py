import requests
from bs4 import BeautifulSoup
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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        urls = [link.get('href') for link in links if link.get('href').startswith('http')]
        return urls
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

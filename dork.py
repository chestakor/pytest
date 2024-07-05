import requests
from bs4 import BeautifulSoup
import time

def process_dork_command(bot, message):
    chat_id = message.chat.id
    dork_query = message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else None

    if not dork_query:
        bot.send_message(chat_id, "Please provide a dork query. Format: /dork your_query")
        return

    start_time = time.time()
    results = search_google_dork(dork_query)
    elapsed_time = time.time() - start_time

    if results:
        response_message = format_response(results, elapsed_time, message.from_user.username)
        bot.send_message(chat_id, response_message, parse_mode='html')
    else:
        bot.send_message(chat_id, "No results found for the given dork query.")

def search_google_dork(query):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for item in soup.find_all('a'):
        href = item.get('href')
        if href and 'url?q=' in href:
            url = href.split('url?q=')[1].split('&sa=U&')[0]
            links.append(url)

    return links

def format_response(results, elapsed_time, username):
    formatted_results = "\n".join(results)
    response = (
        f"🔍 Google Dork Results\n\n"
        f"{formatted_results}\n\n"
        f"－－－－－－－－－－－－－－－－\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return response

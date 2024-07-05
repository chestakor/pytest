import requests
from bs4 import BeautifulSoup
import time

USER_AGENTS = [
    # Add more user agents here
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def process_dork_command(bot, message):
    chat_id = message.chat.id
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.send_message(chat_id, "Please provide a dork query in the format: /dork your_query")
        return

    query = args[1]
    start_time = time.time()

    urls = search_google_dork(query)

    if not urls:
        bot.send_message(chat_id, "No results found for the given dork query.")
    else:
        elapsed_time = time.time() - start_time
        response_message = (
            f"🔍 Google Dork Results\n\n"
            + "\n".join(urls[:20]) +  # Limit to the first 20 results
            f"\n－－－－－－－－－－－－－－－－\n"
            f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
            f"▫️ Checked by: {message.from_user.username}\n"
            f"⚡️ Bot by - AFTAB 👑\n"
            f"－－－－－－－－－－－－－－－－"
        )
        bot.send_message(chat_id, response_message)

def search_google_dork(query):
    headers = {'User-Agent': get_random_user_agent()}
    search_url = f"https://www.google.com/search?q={query}"

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')
    urls = []
    for link in links:
        href = link.get('href')
        if href and href.startswith('/url?q='):
            url = href.split('/url?q=')[1].split('&')[0]
            if not url.startswith('https://www.google.') and not url.startswith('https://accounts.google.'):
                urls.append(url)

    return urls

import re
import telethon
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# Your API ID, hash, and bot token
api_id = '23883349'
api_hash = '9ae2939989ed439ab91419d66b61a4a4'
bot_token = '7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0'

# Create the Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Define a regex pattern to match credit card numbers
cc_pattern = re.compile(r'\b\d{4}[ ]?\d{4}[ ]?\d{4}[ ]?\d{4}\|[0-9]{2}\|[0-9]{2,4}\|[0-9]{3}\b')

async def scrape_cc(group_link, limit):
    await client.start(bot_token=bot_token)

    # Get the group entity
    group = await client.get_entity(group_link)
    
    # Get messages
    result = await client(GetHistoryRequest(
        peer=PeerChannel(group.id),
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    # Extract credit card information
    ccs = []
    for message in result.messages:
        matches = cc_pattern.findall(message.message)
        ccs.extend(matches)
    
    return ccs

def process_scr_command(bot, message):
    chat_id = message.chat.id
    try:
        _, group_link, limit = message.text.split()
        limit = int(limit)
    except ValueError:
        bot.send_message(chat_id, "Please provide the command in the format: /scr group_link limit")
        return

    # Scrape the credit cards
    ccs = client.loop.run_until_complete(scrape_cc(group_link, limit))

    if ccs:
        # Write the scraped credit cards to a file
        file_path = "/mnt/data/scraped_ccs.txt"
        with open(file_path, "w") as f:
            for cc in ccs:
                f.write(f"{cc}\n")
        
        # Send the file to the user
        bot.send_document(chat_id, document=open(file_path, "rb"), caption=f"Scraped {len(ccs)} credit cards from {group_link}")
    else:
        bot.send_message(chat_id, "No credit cards found in the specified range of messages.")

# The part to be added to your main.py
@bot.message_handler(commands=['scr'])
def scr_command(message):
    scraper.process_scr_command(bot, message)

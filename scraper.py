from telethon import TelegramClient, events
from telethon.sessions import StringSession
import re
import os
from telebot import types

# Import the bot instance from main
from main import bot

api_id = '23883349'
api_hash = '9ae2939989ed439ab91419d66b61a4a4'
bot_token = '7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0'
session_string = os.environ.get('SESSION_STRING', None)

client = TelegramClient(StringSession(session_string), api_id, api_hash).start(bot_token=bot_token)

async def scrape_cc(channel, limit):
    cc_pattern = re.compile(r'\b\d{13,19}\|\d{2}\|\d{2,4}\|\d{3,4}\b')
    async for message in client.iter_messages(channel, limit=int(limit)):
        match = cc_pattern.search(message.text)
        if match:
            yield match.group()

def process_scr_command(bot, message):
    chat_id = message.chat.id
    command = message.text.split()
    if len(command) != 3:
        bot.send_message(chat_id, "Please provide the correct format: /scr channel_link number_of_messages")
        return
    
    channel = command[1]
    limit = command[2]
    
    try:
        ccs = list(client.loop.run_until_complete(scrape_cc(channel, limit)))
        if not ccs:
            bot.send_message(chat_id, "No CCs found.")
            return
        
        filename = f"{limit} x {channel.split('/')[-1]}.txt"
        with open(filename, 'w') as file:
            file.write("\n".join(ccs))
        
        with open(filename, 'rb') as file:
            bot.send_document(chat_id, file, caption=f"Target ➔ {channel.split('/')[-1]}\nAmount ➔ {limit}\nFound ➔ {len(ccs)}\nScraped By ➔ {message.from_user.username} [Free]")
        
        os.remove(filename)
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

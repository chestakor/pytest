import re
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.messages import GetHistoryRequest

api_id = '23883349'
api_hash = '9ae2939989ed439ab91419d66b61a4a4'
bot_token = '7237381740:AAGoGZZKQjYUkHBJWd56Xb0fAxJExylP5f0'

async def scrape_cc(group_url, limit):
    # Create the client and connect
    client = TelegramClient('anon', api_id, api_hash)

    await client.start(bot_token=bot_token)
    print("Client Created")

    try:
        entity = await client.get_entity(group_url)
        my_channel = InputPeerChannel(entity.id, entity.access_hash)

        offset_id = 0
        all_messages = []
        total_messages = 0
        total_count_limit = limit

        while True:
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                if len(all_messages) >= total_count_limit:
                    break
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if len(all_messages) >= total_count_limit:
                break

        cc_regex = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
        ccs = []
        for message in all_messages:
            if 'message' in message:
                found_ccs = cc_regex.findall(message['message'])
                for cc in found_ccs:
                    ccs.append(cc.replace(' ', '').replace('-', ''))

        return ccs

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.disconnect()

def process_scr_command(bot, message):
    chat_id = message.chat.id
    try:
        _, group_url, limit = message.text.split()
        limit = int(limit)
    except ValueError:
        bot.send_message(chat_id, "Please provide the correct format: /scr <group_url> <limit>")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ccs = loop.run_until_complete(scrape_cc(group_url, limit))
    if ccs:
        filename = f"{group_url.split('/')[-1]}_ccs.txt"
        with open(filename, 'w') as f:
            f.write("\n".join(ccs))
        bot.send_document(chat_id, document=open(filename, 'rb'))
        response_message = (f"↯ {limit} x {filename}\n\n"
                            f"Target ➔ {group_url.split('/')[-1]}\n"
                            f"Amount ➔ {limit}\n"
                            f"Found 0s ➔ {len(ccs)}\n"
                            f"Scraped By ➔ {message.from_user.username} [Free]\n\n"
                            f"－－－－－－－－－－－－－－－－\n"
                            f"🔹 Total CC Scraped - {len(ccs)}\n"
                            f"⏱️ Time Taken - {loop.time():.2f} seconds\n"
                            f"▫️ Checked by: {message.from_user.username}\n"
                            f"⚡️ Bot by - AFTAB 👑\n"
                            f"－－－－－－－－－－－－－－－－")
        bot.send_message(chat_id, response_message)
    else:
        bot.send_message(chat_id, "No CCs found.")

# Example usage in main.py
# from scraper import process_scr_command

# @bot.message_handler(commands=['scr'])
# def scr_command(message):
#     process_scr_command(bot, message)

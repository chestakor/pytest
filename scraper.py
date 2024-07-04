from telethon import TelegramClient
import re
import asyncio

# Add your own values here
api_id = 23883349
api_hash = '9ae2939989ed439ab91419d66b61a4a4'

client = TelegramClient('scraper', api_id, api_hash)

cc_pattern = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\|(?:0[1-9]|1[0-2])\|[0-9]{2}\|[0-9]{3}\b')

async def scrape_cc(chat_link, num_messages, chat_id, bot):
    await client.start()
    chat = await client.get_entity(chat_link)
    messages = await client.get_messages(chat, limit=num_messages)
    cc_list = []

    for message in messages:
        ccs = cc_pattern.findall(message.message)
        if ccs:
            cc_list.extend(ccs)

    if cc_list:
        file_content = "\n".join(cc_list)
        with open("scraped_ccs.txt", "w") as file:
            file.write(file_content)
        await bot.send_document(chat_id, "scraped_ccs.txt", caption=f"Target ➔ {chat_link.split('/')[-1]}\nAmount ➔ {num_messages}\nFound ➔ {len(cc_list)}")
    else:
        await bot.send_message(chat_id, "No CCs found in the specified messages.")

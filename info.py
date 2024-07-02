import requests
from telebot import types

def get_user_profile_photo(bot, user_id):
    try:
        user_profile_photos = bot.get_user_profile_photos(user_id, limit=1)
        if user_profile_photos.total_count > 0:
            return user_profile_photos.photos[0][0].file_id
    except Exception as e:
        print(f"Failed to get user profile photo: {e}")
    return None

def process_info_command(bot, message):
    chat_id = message.chat.id
    user = message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name

    user_info = (
        f"↯ USER INFORMATION\n"
        f"╔═════════════════╗\n"
        f"• User[NAME] » @{username}\n"
        f"• User[ID] » <code>{user_id}</code>\n"
        f"• Name[TG] » {first_name}\n"
        f"╚═════════════════╝\n"
        f"• Dev » @aftab_kabir\n"
    )

    photo_id = get_user_profile_photo(bot, user_id)
    
    if photo_id:
        bot.send_photo(chat_id, photo_id, caption=user_info, parse_mode='HTML')
    else:
        bot.send_message(chat_id, user_info, parse_mode='HTML')

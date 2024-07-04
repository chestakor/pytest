import requests
import time
from googletrans import Translator

def process_nagad_command(bot, message):
    chat_id = message.chat.id
    numbers = message.text.split()[1:]  # Get the numbers from the command
    if not numbers:
        bot.send_message(chat_id, "Please provide phone numbers in the format: /nagad number1 number2 ...")
        return

    total_numbers = len(numbers)
    start_time = time.time()
    results = []
    translator = Translator()
    initial_message = "↯ NAGAD CHECKER\n\n"
    msg = bot.send_message(chat_id, initial_message + get_footer_info(total_numbers, start_time, message.from_user.username))

    for number in numbers:
        result = check_nagad_number(number, translator)
        results.append(f"Number: {number}\nResult =>\n {result}")
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg.message_id,
            text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_numbers, start_time, message.from_user.username)
        )

def check_nagad_number(number, translator):
    url = f"https://app.mynagad.com:20002/api/user/check-user-status-for-log-in?msisdn={number}"
    headers = {
        "X-KM-User-AspId": "100012345612345",
        "X-KM-User-Agent": "ANDROID/1152",
        "X-KM-DEVICE-FGP": "19DC58E052A91F5B2EB59399AABB2B898CA68CFE780878C0DB69EAAB0553C3C6",
        "X-KM-Accept-language": "bn",
        "X-KM-AppCode": "01",
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if "name" in response_data:
        name_bn = response_data["name"]
        name_en = translator.translate(name_bn, src='bn', dest='en').text
        user_id = response_data["userId"]
        status = response_data["status"]
        user_type = response_data["userType"]
        return (f"Name: {name_bn} ({name_en})\n"
                f"User ID: {user_id}\n"
                f"Status: {status}\n"
                f"User Type: {user_type}")
    elif "reason" in response_data:
        return "No Nagad account found"
    else:
        return response.text

def get_footer_info(total_numbers, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"🔹 Total numbers checked - {total_numbers}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

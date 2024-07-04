import requests
import time

def process_bin_command(bot, message):
    chat_id = message.chat.id
    bin_data = message.text.split()[1:]  # Get the BIN data from the command
    if bin_data:
        total_bins = len(bin_data)
        start_time = time.time()
        results = []
        initial_message = "↯ BIN CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_bins, start_time, message.from_user.username))

        for bin_input in bin_data:
            bin_number = bin_input[:6]
            result = check_bin_details(bin_number)
            results.append(f"BIN: {bin_number}\n{result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_bins, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide BIN details in the format: /bin bin_number")

def check_bin_details(bin_number):
    try:
        response = requests.get(f'https://lookup.binlist.net/{bin_number}')
        if response.status_code == 200:
            bin_info = response.json()
            name = bin_info.get('bank', {}).get('name', 'N/A')
            brand = bin_info.get('scheme', 'N/A').upper()
            type_ = bin_info.get('type', 'N/A').upper()
            country = bin_info.get('country', {}).get('name', 'N/A').upper()
            return (f"Bank: {name}\n"
                    f"Brand: {brand}\n"
                    f"Type: {type_}\n"
                    f"Country: {country}")
        else:
            return "Invalid BIN❌"
    except Exception as e:
        return str(e)

def get_footer_info(total_bins, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total BINs Checked - {total_bins}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

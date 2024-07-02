import re
import time

def process_clean_command(bot, message):
    chat_id = message.chat.id
    start_time = time.time()
    input_text = message.text.split('\n')[1:]  # Get the input text after the command
    
    email_pass_pattern = re.compile(r'[\w\.-]+@[\w\.-]+:\S+')
    cc_pattern = re.compile(r'\d{12,19}\|\d{2,4}\|\d{2,4}\|\d{3,4}')
    
    email_pass_list = email_pass_pattern.findall('\n'.join(input_text))
    cc_list = cc_pattern.findall('\n'.join(input_text))
    
    if email_pass_list:
        cleaned_text = "↯ EMAIL:PASS CLEANED\n\n" + "\n".join(email_pass_list)
    elif cc_list:
        cleaned_text = "↯ CC CLEANED\n\n" + "\n".join(cc_list)
    else:
        cleaned_text = "No valid email:pass or CC data found."

    elapsed_time = time.time() - start_time
    footer = (
        f"\n－－－－－－－－－－－－－－－－\n"
        f"⚫️ Total cleaned - {len(email_pass_list) + len(cc_list)}\n"
        f"⏱️ Time Taken - {elapsed_time:.2f} seconds\n"
        f"▫️ Checked by: {message.from_user.username}\n"
        f"⚡️ Bot by - AFTAB 👑\n"
        f"－－－－－－－－－－－－－－－－"
    )

    bot.send_message(chat_id, cleaned_text + footer)

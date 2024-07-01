def process_help_command(bot, message):
    chat_id = message.chat.id
    help_text = """
Here are the available commands and their usage:

/chk cc|mm|yy|cvc
Example: 
/chk 5314620055099373|01|2027|770
5314620050738926|07|2027|499
...
Use this command to check the validity of credit card information.

/seedr email:password
Example: 
/seedr user@example.com:password123
...
Use this command to check Seedr accounts.

/hoi email:password
Example: 
/hoi user@example.com:password123
...
Use this command to check Hoichoi accounts.

/crunchy email:password
Example: 
/crunchy user@example.com:password123
...
Use this command to check Crunchyroll accounts.

/grab url
Example: 
/grab https://example.com/checkout?cs=cs_example
...
Use this command to grab CS and PK details from a provided URL.

/nonsk1 cc|mm|yy|cvc
Example: 
/nonsk1 5314620055099373|01|2027|770
...
Use this command to check credit card details with the nonsk1 method.

/nonsk2 cc|mm|yy|cvc
Example: 
/nonsk2 5314620055099373|01|2027|770
...
Use this command to check credit card details with the nonsk2 method.

If any problem contact @aftab_kabir

Owner: Aftab👑
"""
    bot.send_message(chat_id, help_text)

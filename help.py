def process_help_command(bot, message):
    help_text = (
        "### [GATES]\n\n"
        "**STRIPE Charge - [ TEST ]**\n"
        "- **Format:** /chk cc|mon|year|cvv\n"
        "- **Gateway:** Stripe » FREE\n"
        "- **Updated:** 02:54:04 14-02-2024\n\n"
        
        "**NONSK CHECKER-1 - [ TEST ]**\n"
        "- **Format:** /nonsk1 cc|mon|year|cvv\n"
        "- **Gateway:** Stripe » FREE\n"
        "- **Updated:** 12:58:42 10-02-2024\n\n"
        
        "**NONSK  CHECKER-2 - [ TEST ]**\n"
        "- **Format:** /nonsk2 cc|mon|year|cvv\n"
        "- **Gateway:** Stripe » FREE\n"
        "- **Updated:** 17:40:35 20-02-2024\n\n"
        
        "(MORE COMING SOON)\n\n"
        
        "### [TOOL]\n\n"
        "ᅳᅳᅳᅳᅳᅳᅳᅳᅳᅳᅳᅳᅳ\n"
        "**Website:** Seedr\n"
        "- **Format:** /seedr email:pass\n"
        "- **Status:** ACTIVE ✅\n\n"
        
        "**Website:** Crunchyroll\n"
        "- **Format:** /crunchy email:pass\n"
        "- **Status:** ACTIVE ✅\n\n"
        
        "**Website:** Hoichoi\n"
        "- **Format:** /hoi email:pass\n"
        "- **Status:** ACTIVE ✅\n\n"
        
        "**Website:** Zee5 Global\n"
        "- **Format:** /z email:pass\n"
        "- **Status:** Coming Soon 🌦\n\n"
        
        "**Website:** Stripe CS PK GRABBER\n"
        "- **Format:** /grab url\n"
        "- **Status:** ACTIVE ✅\n\n"
        
        "If any problem contact @aftab_kabir\n\n"
        "Owner: Aftab👑"
    )
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# In the main script, add the following handler:

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# 🔴 YOUR TOKEN
TOKEN = "8516809481:AAHh7Iv34zy1Iql_h_khrr8AzxTPvC0Uc4Q"

bot = telebot.TeleBot(TOKEN)

# 🔴 YOUR LIVE APP URL (From the tunnel)
APP_URL = "https://c2f0d31be8a98e.lhr.life" 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    
    # Create the "Open App" button
    markup = InlineKeyboardMarkup()
    # The WebAppInfo tells Telegram this button opens a Mini App
    btn_app = InlineKeyboardButton("🚀 Open Miner", web_app=WebAppInfo(url=APP_URL))
    markup.add(btn_app)
    
    text = (
        f"👋 **Welcome, {user_first_name}!**\n\n"
        f"Start mining crypto now inside Telegram.\n"
        f"Click the button below to launch the app."
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

print("🤖 Bot is running...")
bot.infinity_polling()	

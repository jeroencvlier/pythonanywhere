import os
import telebot
from dotenv import load_dotenv, find_dotenv


bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

def send_mess(message):
    bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), message)
    

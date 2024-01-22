import os
import telebot

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))

def send_message(message):
    bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), message)
    
    

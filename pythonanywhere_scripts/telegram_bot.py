import os
import telebot
import logging
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


def send_mess(message):
    logging.info(f"Sending message: {message}")
    bot.send_message(os.getenv("TELEGRAM_CHAT_ID"), message)

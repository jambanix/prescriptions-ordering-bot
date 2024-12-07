
import logging
from requests import post
from os import getenv

def send_message(message: str):
    """
    Send message using Telegram to notify of an event. Details taken from environment variables

    :param message: message to send
    """
    URL = f"https://api.telegram.org/bot{getenv('TELEGRAM_API_KEY')}/sendMessage"
    data = {
        "chat_id": getenv("TELEGRAM_ID"),
        "text": message
    }
    try:
        response = post(URL, data=data)
        if response.ok:
            logging.info("Telegram notification sent")
        else:
            logging.error("Failed to send Telegram notification")
            logging.error(response.text)
    except Exception as e:
        logging.error("Failed to send Telegram notification")
        logging.error(str(e))

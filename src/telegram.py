
from requests import post
import logging

def send_message(api_key, chat_id, message):
    URL = f"https://api.telegram.org/bot{api_key}/sendMessage"
    data = {
        "chat_id": chat_id,
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

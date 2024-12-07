import logging
from dotenv import load_dotenv
from src.bot import main
from os import path

DIRECTORY = path.dirname(path.abspath(__file__))
DATA_FILE = f"{DIRECTORY}/data/prescriptions.json"
ENV = f"{DIRECTORY}/data/.env"
LOG_FILE = f"{DIRECTORY}/log/bot.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
      logging.FileHandler(LOG_FILE),
      logging.StreamHandler()])

if __name__ == "__main__":
    logging.info("Started")
    load_dotenv(ENV)
    main(DATA_FILE)




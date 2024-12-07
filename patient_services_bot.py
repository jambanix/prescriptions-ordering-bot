import logging
from dotenv import load_dotenv
from src.bot import main


DATA_FILE = "data/prescriptions.json"
ENV = "data/.env"
LOG_FILE = "log/bot.log"

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




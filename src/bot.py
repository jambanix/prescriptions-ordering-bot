from dotenv import load_dotenv
from os import getenv
from json import load, dump
from datetime import datetime, timedelta
import logging
from .telegram import send_message
from .ordering import order_prescriptions

DATA_FILE = "data/prescriptions.json"
ENV = "data/.env"

def calculate_due_date(last_ordered, frequency):
    return (datetime.strptime(last_ordered, "%Y-%m-%d") + timedelta(days=frequency)).date()

def check_if_due(prescription: dict):
    return datetime.today().date() == calculate_due_date(prescription["last_ordered"], prescription["frequency"])

def init():
  load_dotenv(ENV)
  logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  handlers=[
    logging.FileHandler("log/bot.log"),
    logging.StreamHandler()])
  logging.info("Bot initialised")

def load_prescriptions(filename=DATA_FILE):
  try:
    with open(filename) as f:
      data = load(f)
      if data:
        logging.info("Prescriptions loaded")
        return data
  except FileNotFoundError:
    logging.error(f"Prescriptions file not found at {filename}")
    return

def get_due_prescriptions(prescriptions: list):
  try:
    out = []
    for prescription in prescriptions:
      if check_if_due(prescription):
        logging.info(f"{prescription['name']} is due")
        out.append(prescription)
      else:
        logging.info(f"{prescription['name']} is not due: next due date is {calculate_due_date(prescription['last_ordered'], prescription['frequency'])}")
    return out
  except Exception as e:
    logging.error(f"Could not check if prescriptions due using data {prescriptions}")
    logging.error(str(e))
    send_message("FATAL: failed to check if prescriptions are due")
    return

  
def update_file(prescriptions):
  old = load_prescriptions()
  for prescription in prescriptions:
    target = old.index(prescription)
    old[target]["last_ordered"] = datetime.today().date().strftime("%Y-%m-%d")

  with open("data/prescriptions.json", "w") as f:
    dump(old, f)
    logging.info("Prescriptions file updated")
    for prescription in prescriptions:
      logging.info(f"{prescription['name']} next due on {calculate_due_date(prescription['last_ordered'], prescription['frequency'])}")

def run():
  init()
  prescriptions = load_prescriptions()
  if not prescriptions:
    send_message("FATAL: failed to load prescriptions")
    exit(1)
  due_prescriptions = get_due_prescriptions(prescriptions)
  if not due_prescriptions:
    exit(0)
  ordered = order_prescriptions(getenv("LOGIN"), getenv("PASSWORD"), due_prescriptions)
  if not ordered:
    send_message("FATAL: failed to order prescriptions")
    exit(1)
  update_file(ordered)
  send_message(getenv("TELEGRAM_API"), getenv("TELEGRAM_ID"), "Prescriptions ordered successfully: " + "\n- ".join([prescription["name"] for prescription in ordered]))
  logging.info("Bot completed successfully")
  exit(0)
  
  
import logging
from json import load, dump
from datetime import datetime, timedelta
from .telegram import send_message
from .ordering import order_prescriptions
from .google_calendar import create_event

def __calculate_due_date(last_ordered: str, frequency: int):
    """
    Calculate the due date of prescription based on the date it was last ordered and its frequency

    :param last_ordered: date the prescription was last ordered
    :param frequency: how often the prescription should be ordered
    :return: date the prescription is next due
    :rtype: datetime
    """
    return (datetime.strptime(last_ordered, "%Y-%m-%d") + timedelta(days=frequency)).date()

def __check_if_due(prescription: dict):
    """
    Checks if a prescription is due to be ordered based on the date it was last ordered and its frequency

    :param prescription: prescription to check
    :return: whether the prescription is due
    :rtype: bool
    """
    return datetime.today().date() == __calculate_due_date(prescription["last_ordered"], prescription["frequency"])

def __load_prescriptions(filename: str):
  """
  Load the prescriptions from file - contians name, dose, frequency and date last ordered

  :param filename: file to load prescriptions from
  :return: prescriptions
  :rtype: list
  """
  try:
    with open(filename) as f:
      data = load(f)
      if data:
        logging.info("Prescriptions loaded")
        return data
  except FileNotFoundError:
    logging.error(f"Prescriptions file not found at {filename}")
    return

def __get_due_prescriptions(prescriptions: list):
  """
  Iterate over prescriptions loaded from file and check if any are due to be ordered

  :param prescriptions: prescriptions to check
  :return: prescriptions that are due
  :rtype: list
  """
  try:
    out = []
    for prescription in prescriptions:
      if __check_if_due(prescription):
        logging.info(f"{prescription['name']} is due")
        out.append(prescription)
      else:
        logging.info(f"{prescription['name']} is not due: next due date is {__calculate_due_date(prescription['last_ordered'], prescription['frequency'])}")
    return out
  except Exception as e:
    logging.error(f"Could not check if prescriptions due using data {prescriptions}")
    logging.error(str(e))
    send_message("ERROR: failed to check if prescriptions are due")
    return

  
def __update_file(prescriptions: list):
  """
  Update the last oredered date in the file of prescriptions that have been ordered

  :param prescriptions: prescriptions that have been ordered
  :return: whether the file was updated successfully
  :rtype: bool
  """
  try:
    old = __load_prescriptions()
    for prescription in prescriptions:
      target = old.index(prescription)
      old[target]["last_ordered"] = datetime.today().date().strftime("%Y-%m-%d")

    with open("data/prescriptions.json", "w") as f:
      dump(old, f)
      logging.info("Prescriptions file updated")
      for prescription in prescriptions:
        logging.info(f"{prescription['name']} next due on {__calculate_due_date(prescription['last_ordered'], prescription['frequency'])}")
    return True
  except IOError as e:
    logging.error("Could not update prescriptions file")
    logging.error(prescriptions)
    logging.error(str(e))
    send_message("ERROR: failed to update prescriptions file")
    return False


def main(data_file: str):
  """
  The main execution of the bot - loads prescriptions, checks if any are due, orders them and updates the file with any that have been ordered

  :param data_file: file to load prescriptions from
  """
  prescriptions = __load_prescriptions(data_file)
  if not prescriptions:
    send_message("ERROR: failed to load prescriptions")
    exit(1)
  due_prescriptions = __get_due_prescriptions(prescriptions)
  if not due_prescriptions:
    exit(0)
  ordered = order_prescriptions(due_prescriptions)
  if not ordered:
    send_message("ERROR: failed to order prescriptions")
    exit(1)
  __update_file(ordered)
  send_message("Prescriptions ordered successfully: " + "\n- ".join([prescription["name"] for prescription in ordered]))
  if create_event(ordered):
    logging.info("Created Gmail calendar event successfully")
  else:
    logging.error("Failed to create Gmail calendar event")
    send_message("ERROR: failed to create Gmail calendar event")
  logging.info("Bot finished")
  exit(0)
  
  
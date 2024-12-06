from requests import Session
from time import sleep
import logging
from json import dumps

HOME = "https://www.patient-services.co.uk/"
LOGIN = "https://www.patient-services.co.uk/login"
ORDER = "https://www.patient-services.co.uk/prescriptions/order"
# ORDER = "https://www.patient-services.co.uk/prescriptions/confirm-order"

def login(session: Session, username: str, password: str) -> bool:
    logging.info("Requesting home page")
    response = session.get(HOME, verify=False)
    if not response.ok:
        logging.error("Could not access home page")
        logging.error(response.text)
        return False

    logging.info("Logging in")
    response = session.post(LOGIN, data={"username": username, "password": password}, verify=False)
    if not response.ok:
        logging.error("Could not log in")
        logging.error(response.text)
        return False
    return True

def send_prescription_request(session: Session, payload: dict) -> bool:
    logging.info("Requesting prescriptions")
    response = session.post(ORDER, data=payload, verify=False)
    if response.ok:
        logging.info("Prescriptions requested")
        logging.info(response.text)
        return True
    else:
        logging.error("Could not request prescriptions")
        logging.error(response.text)
        return False
    

def order_prescriptions(username: str, password: str, due_prescriptions: list, attempt=0, max_attempts=3, wait=10):
    if attempt > max_attempts:
        logging.error("Max attempts reached")
        return

    def rerun():
        logging.info(f"Retrying in {wait} minutes")
        sleep(wait * 60)
        return order_prescriptions(due_prescriptions, attempt + 1)

    # create payload
    payload = {
        "requestSummaryJson":dumps({
            "repeatIds": [],
            "message": "",
            "additionalRequest": "\r\n".join([f'{prescription["name"]} {prescription["dose"]}' for prescription in due_prescriptions])}),
        "selectedRepeatsJson": dumps([])
        }
    
    # log in and send request
    try:
        session = Session()
        if not login(session, username, password):
            return rerun()
        if not send_prescription_request(session, payload):
            return rerun()
        return due_prescriptions
    except Exception as e:
        logging.error(f"Failed to request prescriptions")
        logging.error(str(e))
        return rerun()
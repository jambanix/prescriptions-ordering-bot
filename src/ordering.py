import logging
from requests import Session
from time import sleep
from json import dumps
from os import getenv

HOME = "https://www.patient-services.co.uk/"
LOGIN = "https://www.patient-services.co.uk/login"
ORDER = "https://www.patient-services.co.uk/prescriptions/order"

def __login(session: Session, username: str, password: str):
    """
    Login to the patient-services website using the provided username and password

    :param session: requests session
    :param username: username to login with
    :param password: password to login with
    :return: whether the login was successful
    :rtype: bool
    """
    logging.info("Requesting home page")
    response = session.get(HOME, verify="www-patient-services-co-uk-chain.pem")
    if not response.ok:
        logging.error("Could not access home page")
        logging.error(response.text)
        return False

    logging.info("Logging in")
    response = session.post(LOGIN, data={"username": username, "password": password}, verify="www-patient-services-co-uk-chain.pem")
    if not response.ok:
        logging.error("Could not log in")
        logging.error(response.text)
        return False
    return True

def __send_prescription_request(session: Session, payload: dict):
    """
    Send the POST request to the prescription ordering endpoint with the prescriptions needing ordered

    :param session: requests session
    :param payload: data to send with the request
    :return: whether the request was successful
    :rtype: bool
    """
    logging.info("Requesting prescriptions")
    response = session.post(ORDER, data=payload, verify="www-patient-services-co-uk-chain.pem")
    if response.ok:
        logging.info("Prescriptions requested")
        logging.info(response.text)
        return True
    else:
        logging.error("Could not request prescriptions")
        logging.error(response.text)
        return False
    

def order_prescriptions(due_prescriptions: list, attempt=0, max_attempts=3, wait=10):
    """
    Login to the website, send the prescription request and return the prescriptions that were ordered.
    Rerun the function after a wait period if the request fails

    :param due_prescriptions: prescriptions that are due to be ordered
    :param attempt: current attempt number
    :param max_attempts: maximum number of attempts to make
    :param wait: time to wait between attempts in minutes
    :return: prescriptions that were ordered
    :rtype: list
    """
    def rerun():
        """
        Rerun the parent function after a wait period
        """
        logging.info(f"Retrying in {wait} minutes")
        sleep(wait * 60)
        return order_prescriptions(due_prescriptions, attempt + 1)

    if attempt > max_attempts:
        logging.error("Max attempts reached")
        return
    
    logging.info(f"Attempting to order prescriptions: attempt {attempt + 1} of {max_attempts}")
    payload = {
        "requestSummaryJson":dumps({
            "repeatIds": [],
            "message": "",
            "additionalRequest": "\r\n".join([f'{prescription["name"]} {prescription["dose"]}' for prescription in due_prescriptions])}),
        "selectedRepeatsJson": dumps([])
        }
    try:
        session = Session()
        if not __login(session, getenv("LOGIN"), getenv("PASSWORD")):
            return rerun()
        if not __send_prescription_request(session, payload):
            return rerun()
        return due_prescriptions
    
    except Exception as e:
        logging.error(f"Failed to request prescriptions")
        logging.error(str(e))
        return rerun()
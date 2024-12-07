import logging
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event, PopupReminder
from datetime import datetime, timedelta

def __working_days_date(start, working_days):
    """
    Caluculate the date after a number of working days

    :param start: date to start from
    :param working_days: number of working days to wait
    :return: date after working days
    :rtype: datetime
    """
    incremented = 0
    while incremented < working_days:
        start += timedelta(days=1)
        if start.weekday() < 5:
            incremented += 1
    return start


def create_event(prescriptions_ordered, start_from=None, working_days=2):
    """
    Create Gmail calendar event for collecting prescription

    :param prescriptions_ordered: list of prescriptions to collect
    :param start_from: date to start from
    :param working_days: number of working days to wait

    """
    try:
      calendar = GoogleCalendar(credentials_path="data/token.pickle")
      body = f"Collect: {",".join([prescription["name"] for prescription in prescriptions_ordered])}"
      if not start_from:
          start_from = datetime.today().date()
      else:
          start_from = datetime.strptime(start_from, "%Y-%m-%d").date()
      collect_date = __working_days_date(start_from, working_days)
      collect_datetime = datetime(collect_date.year, collect_date.month, collect_date.day, 16)
      logging.info(f"Creating event for {collect_date}")
      event = Event(
          summary="Collect Prescription",
          description=body,
          start=collect_datetime,
          end=collect_datetime + timedelta(hours=1),
          reminders=[
              PopupReminder(minutes_before_start=60),
              PopupReminder(minutes_before_start=(8*60))
          ]
      )
      calendar.add_event(event)
      logging.info("Event created successfully")
      return True
    except Exception as e:
        logging.error("Failed to create calendar event")
        logging.error(str(e))
        return False

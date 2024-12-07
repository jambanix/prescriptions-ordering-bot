from unittest import TestCase, main
from src import bot
from datetime import datetime
from src import google_calendar

# tests on 06-dec-2024
class TestCheckIfDue(TestCase):
  def test_due(self):
    self.assertFalse(bot.__check_if_due({"last_ordered": "2024-12-01", "frequency": 28}))
    self.assertFalse(bot.__check_if_due({"last_ordered": "2024-11-17", "frequency": 28}))
    self.assertFalse(bot.__check_if_due({"last_ordered": "2024-11-10", "frequency": 28}))
    self.assertTrue(bot.__check_if_due({"last_ordered": "2024-11-08", "frequency": 28}))

class TestCalculateDueDate(TestCase):
  def test_due(self):
    self.assertEqual(bot.__calculate_due_date("2024-12-01", 28), datetime(2024, 12, 29).date())
    self.assertEqual(bot.__calculate_due_date("2024-11-17", 28), datetime(2024, 12, 15).date())
    self.assertEqual(bot.__calculate_due_date("2024-11-10", 28), datetime(2024, 12, 8).date())
    self.assertEqual(bot.__calculate_due_date("2024-11-03", 28), datetime(2024, 12, 1).date())
    self.assertEqual(bot.__calculate_due_date("2024-10-27", 28), datetime(2024, 11, 24).date())
    self.assertEqual(bot.__calculate_due_date("2024-11-08", 28), datetime(2024, 12, 6).date())

class TestWorkingDaysCalc(TestCase):
  def test_working_days_date(self):
    self.assertEqual(google_calendar.__working_days_date("2024-12-07", 2), datetime(2024, 12, 10).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-08", 2), datetime(2024, 12, 10).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-09"), datetime(2024, 12, 11).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-10"), datetime(2024, 12, 12).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-11"), datetime(2024, 12, 13).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-12"), datetime(2024, 12, 16).date())
    self.assertEqual(google_calendar.__working_days_date("2024-12-13"), datetime(2024, 12, 17).date())
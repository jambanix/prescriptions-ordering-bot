from unittest import TestCase, main
from src import bot
from datetime import datetime

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

main(verbosity=2)
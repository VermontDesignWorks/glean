"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from gleanevent.models import GleanEvent
from django.utils import timezone
import datetime


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class GleanEventTests(TestCase):
	def test_upcomming_event(self):
		now = timezone.now()
		upcomming_glean = GleanEvent(date = now + datetime.timedelta(days=5))
		self.assertEqual(upcomming_glean.upcomming_event(), True)

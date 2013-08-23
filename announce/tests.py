"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from test_functions import *

class AnnouncementTests(TestCase):
	def test_populate_recipients_method(self):
		county = create_county()
		for i in range(20):
			user, profile = create_user_and_profile()
			profile.counties.add(county)
		for i in range(3):
			user, profile = create_user_and_profile(preferred_method='2')
			profile.counties.add(county)
		glean = create_glean()
		glean.counties.add(county)
		announce = create_announcement(glean=glean, member_organization=glean.member_organization)
		self.assertEqual(announce.email_recipients.count(), 0)
		self.assertEqual(announce.phone_recipients.count(), 0)
		announce.populate_recipients()
		self.assertEqual(announce.email_recipients.count(), 20)
		self.assertEqual(announce.phone_recipients.count(), 3)
		
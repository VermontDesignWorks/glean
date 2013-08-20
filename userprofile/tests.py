"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User
from userprofile.models import Profile
from gleanevent.models import PostGlean


def create_volunteer_user_object():
	return User.objects.create_user("TestUser","TestUser@example.com","password")

def create_profile(user):
	return Profile(user=user, first_name="John", last_name="Doe")

def create_post_glean(user, hours):
	return PostGlean(user=user, hours = hours)

class TestDefinitions(TestCase):
	def test_create_volunteer_user_object(self):
		user = create_volunteer_user_object()
		profile = create_profile(user)
		pg1 = create_post_glean(user, 1)
		pg2 = create_post_glean(user, 3)
		self.assertEqual(user.username, "TestUser")
		self.assertEqual(profile.user, user)
		self.assertEqual(pg1.user, user)
		self.assertEqual(pg1.hours, 1)
		self.assertEqual(pg2.hours, 3)

class UserProfileMethods(TestCase):
	def testing_the_get_volunteer_hours_method(self):
		#why does this fail?
		user = create_volunteer_user_object()
		profile = create_profile(user)
		pg1 = create_post_glean(user, 1)
		pg2 = create_post_glean(user, 2)
		self.assertEqual(profile.get_hours(), 3)

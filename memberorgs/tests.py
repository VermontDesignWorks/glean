"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest

from memberorgs.models import MemOrg

class MemOrgModelTests(TestCase):
	def setUp(self):
		MemOrg.objects.create(name="member organization 1")
		MemOrg.objects.create(name="123(*&$%*&^! '@'#.\]/][")

	### because who hasn't written a crappy unicode method? ###
	def makeSureYourUnicodeSettingsDontReturnAnError(self):
		org1 = MemOrg.objects.filter(name="member organization 1")
		org2 = MemOrg.objects.filter(name="123(*&$%*&^! '@'#.\]/][")
		assert org1.__unicode__() == u"member organization 1"
		assert org2.__unicode__() == u"123(*&$%*&^! '@'#.\]/]["

	def otherMethod(self):
		pass
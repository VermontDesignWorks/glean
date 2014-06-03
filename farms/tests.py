"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import unittest
from django.http import HttpRequest
from announce.models import Template
from memberorgs.models import MemOrg
from userprofile.models import Profile
from farms.models import Farm
from farms.views import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class FarmMenipulationTesting(TestCase):
    def testing_if_create_farm_returns_html(self):
        request = HttpRequest
        response = NewFarm.as_view()
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertTrue(self.assertTrue(response.content.startswith(b'<DOCTYPE html>')))
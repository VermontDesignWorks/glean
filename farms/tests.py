"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from django.http import HttpRequest
from announce.models import Template
from memberorgs.models import MemOrg
from userprofile.models import Profile
from farms.models import Farm
from farms.views import *
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test.client import RequestFactory
from test_functions import *
from farms.forms import *
from constants import STATES, COLORS, LINE_TYPE


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class FarmMenipulationTesting(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.groups = test_groups()
        self.county = create_county()
        self.memorg = create_memorg()
        self.memorg.counties.add(self.county)
        # Salvation Farms Admin
        # self.user = create_salvation_farms_admin(self.groups.Salvation_Farms_Administrator, self.memorg)
        # Gleaning Coordinator
        self.user = create_special_user(self.groups.Member_Organization_Glean_Coordinator, self.memorg)
        # regular volunteer
        # self.user = create_user_and_profile(member_organization=self.memorg)

    def test_new_farm_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/farms/newfarm')

        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = NewFarm.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_new_farm_form(self):
        view = NewFarm()
        form = NewFarmForm(
            name="New Farm",
            description="A new farm",
            address_one="594 cochran rd",
            address_two="",
            city="Morrisville",
            state=STATES[0],
            zipcode="05661",
            physical_is_mailing=True,
            mailing_address_one="",
            mailing_address_two="",
            mailing_city="",
            mailing_state=STATES[0],
            mailing_zip="",
            phone_1="8025786266",
            phone_1_type=LINE_TYPE[0],
            phone_2="",
            phone_2_type=LINE_TYPE[0],
            email="joshua.lucier@gmail.com",
            directions="Dude these are the directions.",
            instructions="Dude These are the instructions.",
            counties=self.county,
        )
        form.member_organization.add(self.user.profile.member_organization)
        saved = view.form_valid(form)
        self.assertEqual(True, saved)
        farm = Farm.objects.get(pk=1)
        self.assertEqual(farm.name, "New Farm")
        self.assertValid

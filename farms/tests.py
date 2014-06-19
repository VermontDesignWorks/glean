"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django import forms
from django.db import models
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


class FarmManipulationTesting(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.groups = test_groups()
        self.county = create_county()
        self.memorg = create_memorg()
        self.memorg.counties.add(self.county)
        self.farm = create_farm(self.memorg)
        # Salvation Farms Admin
        # self.user = create_salvation_farms_admin(self.groups.Salvation_Farms_Administrator, self.memorg)
        # Gleaning Coordinator
        self.user = create_special_user(self.groups.Member_Organization_Glean_Coordinator, self.memorg)
        # regular volunteer
        # self.user = create_user_and_profile(member_organization=self.memorg)
        self.data = {
            "name": "New Farm",
            "description": "A new farm",
            "address_one": "594 cochran rd",
            "address_two": "",
            "city": "Morrisville",
            "state": "VT",
            "zipcode": "05661",
            "physical_is_mailing": True,
            "mailing_address_one": "",
            "mailing_address_two": "",
            "mailing_city": "",
            "mailing_state": "VT",
            "mailing_zip": "",
            "phone_1": "8025786266",
            "phone_1_type": "C",
            "phone_2": "",
            "phone_2_type": "C",
            "email": "jmluc123@gmail.com",
            "directions": "Dude these are the directions.",
            "instructions": "Dude These are the instructions.",
            "counties": self.county.pk
            }
        self.kwargs = {'instance': self.farm, 'prefix': None, 'initial': {}}

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
        form = NewFarmForm(data={
            "name": "New Farm",
            "description": "A new farm",
            "address_one": "594 cochran rd",
            "address_two": "",
            "city": "Morrisville",
            "state": "VT",
            "zipcode": "05661",
            "physical_is_mailing": True,
            "mailing_address_one": "",
            "mailing_address_two": "",
            "mailing_city": "",
            "mailing_state": "VT",
            "mailing_zip": "",
            "phone_1": "8025786266",
            "phone_1_type": "C",
            "phone_2": "",
            "phone_2_type": "C",
            "email": "jmluc123@gmail.com",
            "directions": "Dude these are the directions.",
            "instructions": "Dude These are the instructions.",
            "counties": self.county.pk
            })
        form.data["member_organization"] = [self.user.profile.member_organization.pk]
        form.is_valid()
        form.errors
        view = NewFarm()
        response = form.save()
        self.assertEqual(form.is_valid(), True)
        thisfarm = Farm.objects.get(name="New Farm")
        self.assertEqual(thisfarm.name, "New Farm")

    def test_edit_farm_view(self):
        # Create an instance of a GET request.
        pk = str(Farm.objects.first().pk)
        request = self.factory.get('/farms/'+pk+'/edit/')
        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user
        response = NewFarm.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_farm_form(self, *args, **kwargs):
        form = EditFarmForm(data=self.data)
        form.data["instructions"] = "New Instructions"
        form.is_valid()
        form.errors
        response = form.save()
        self.assertEqual(form.is_valid(), True)
        thisfarm = Farm.objects.get(name="New Farm")
        self.assertEqual(thisfarm.instructions, "New Instructions")

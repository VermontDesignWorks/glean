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
from recipientsite.models import RecipientSite
from distro.models import Distro
from distro.forms import DistroEntryForm
import datetime

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class DistroEntryTesting(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.groups = test_groups()
        self.county = create_county()
        self.memorg = create_memorg()
        self.memorg.counties.add(self.county)
        self.farm = create_farm(self.memorg)
        self.location = create_location(self.farm)
        self.site = create_recipient_site(self.memorg)
        # Salvation Farms Admin
        # self.user = create_salvation_farms_admin(self.groups.Salvation_Farms_Administrator, self.memorg)
        # Gleaning Coordinator
        self.user = create_special_user(self.groups.Member_Organization_Glean_Coordinator, self.memorg)
        # regular volunteer
        # self.user = create_user_and_profile(member_organization=self.memorg)

    def test_Edit_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/distribution/edit/')

        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = NewFarm.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_Entry_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('/distribution/entry/')

        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = NewFarm.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_distro_entry_form(self):
        form = DistroEntryForm(data={"date_d": "2014-06-24",
                                     "del_or_pick": 'd',
                                     "recipient": RecipientSite.objects.first().pk,
                                     "field_or_farm": 'p',
                                     "date": "2014-06-20",
                                     "farm": Farm.objects.first().pk,
                                     "crops": "raddishes",
                                     "pounds": "123",
                                     "other": "123",
                                     "containers": "123",
                                     "member_organization": self.user.profile.member_organization.pk
                                     })
        form.is_valid()
        form.errors
        response = form.save(commit=False)
        response.member_organization = self.user.profile.member_organization
        response.save()
        self.assertEqual(form.is_valid(), True)
        thisdistro = Distro.objects.get(field_or_farm='p')
        self.assertEqual(thisdistro.field_or_farm, 'p')

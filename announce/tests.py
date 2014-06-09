"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date, timedelta

from django.contrib.sites.models import Site
from django.test import TestCase

from gleanevent.models import GleanEvent
from memberorgs.models import MemOrg
from announce.forms import *
from announce.views import *

from test_functions import *
from mail_system import render_email, mail_from_source

from django.test.client import RequestFactory


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
        glean.counties = county
        glean.save()
        announce = create_announcement(
            glean=glean, member_organization=glean.member_organization)
        self.assertEqual(announce.email_recipients.count(), 0)
        self.assertEqual(announce.phone_recipients.count(), 0)
        announce.populate_recipients()
        self.assertEqual(announce.email_recipients.count(), 20)
        self.assertEqual(announce.phone_recipients.count(), 3)

    def test_uninvite_user_method(self):
        announce = create_announcement()
        user_email, profile_email = create_user_and_profile()
        user_phone, profile_phone = create_user_and_profile(
            preferred_method='2')
        announce.email_recipients.add(user_email)
        announce.phone_recipients.add(user_phone)
        self.assertEqual(announce.email_recipients.count(), 1)
        self.assertEqual(announce.phone_recipients.count(), 1)
        announce.uninvite_user(user_email)
        self.assertEqual(announce.email_recipients.count(), 0)
        announce.uninvite_user(user_phone)
        self.assertEqual(announce.phone_recipients.count(), 0)

    def test_announcement_default_template_on_create(self):
        announce = create_announcement()
        self.assertIsNotNone(announce.template)


class MailSystemTests(TestCase):
    """Because this system needs some double checking"""

    @classmethod
    def setUpClass(cls):
        site = Site.objects.create(domain="vermontgleaningcollective.org")

    def setUp(self):
        self.site = Site.objects.get(pk=1)
        self.county = create_county()
        self.glean = create_glean(
            counties=self.county,
            date=date.today() + timedelta(days=3))
        self.announcement = create_announcement(glean=self.glean)
        self.glean.member_organization = self.announcement.member_organization
        self.glean.save()
        self.user, self.profile = create_user_and_profile()

    def test_render_email(self):
        template = self.glean.member_organization.create_default_template()
        body = render_email(self.announcement, self.profile)
        self.assertEqual(
            type(body),
            str,
            "Body is not a string (or we made it to python 3!"
            " Body is of type: {0}".format(type(body))
        )

    def test_mail_from_source_no_recipients(self):
        county = create_county()
        user, profile = create_user_and_profile()
        profile.counties.add(county)
        glean = create_glean(
            created_by=user,
            date=date.today() + timedelta(days=3),
            counties=county
        )
        announce = create_announcement(glean=glean)
        self.assertEqual(mail_from_source(announce), 0)

    def test_mail_from_source_testing_email(self):
        county = create_county()
        user, profile = create_user_and_profile()
        profile.counties.add(county)
        glean = create_glean(
            created_by=user,
            date=date.today() + timedelta(days=3),
            counties=county
        )
        announce = create_announcement(glean=glean)
        memo = announce.member_organization
        memo.testing_email = "test@example.com"
        memo.testing = True
        memo.save()
        self.assertEqual(mail_from_source(announce), 1)

    def test_mail_from_source_normal_function(self):
        county = create_county()
        user, profile = create_user_and_profile()
        glean = create_glean(
            created_by=user,
            date=date.today() + timedelta(days=3),
            counties=county
        )
        announce = create_announcement(glean=glean)
        memo = announce.member_organization
        memo.testing = False
        memo.save()

        user, profile = create_user_and_profile()
        profile.counties.add(county)
        user, profile = create_user_and_profile()
        profile.counties.add(county)
        user, profile = create_user_and_profile()
        profile.counties.add(county)
        self.assertEqual(mail_from_source(announce), 3)


class NewTemplateTest(TestCase):
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
        self.data = {
            "template_name": "New Template",
            "member_organization": self.memorg.pk,
            "body": "This is a test form",
            "default": False
            }

    def test_new_template_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('announce/templates/new/')

        # Recall that middleware are not suported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = NewTemplate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_new_template_form(self):
        form = NewFarmForm(self.data)
        form.data["member_organization"] = self.user.profile.member_organization.pk
        form.is_valid()
        form.errors
        view = NewFarm()
        response = form.save()
        self.assertEqual(form.is_valid(), True)
        thisfarm = Farm.objects.get(name="New Template")
        self.assertEqual(thisfarm.name, "New Template")

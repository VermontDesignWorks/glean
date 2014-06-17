"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import date, timedelta

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from announce.views import AnnouncementListView
from gleanevent.models import GleanEvent
from memberorgs.models import MemOrg

from test_functions import *
from mail_system import render_email, mail_from_source


class AnnouncementTests(TestCase):
    def test_populate_recipients_method(self):
        county = create_county()
        for i in range(20):
            user = create_user_and_profile(
                tasks_gleaning=True
            )

            user.profile.counties.add(county)
        for i in range(3):
            user = create_user_and_profile(
                preferred_method='2',
                tasks_gleaning=True
            )
            user.profile.counties.add(county)
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
        user_email = create_user_and_profile()
        user_phone = create_user_and_profile(
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
        self.user = create_user_and_profile()

    def test_render_email(self):
        template = self.glean.member_organization.create_default_template()
        body = render_email(self.announcement, self.user.profile)
        self.assertNotEqual(
            body,
            "",
            "Body is not a string (or we made it to python 3!"
            " Body is of type: {0}".format(type(body))
        )

    def test_mail_from_source_no_recipients(self):
        county = create_county()
        user = create_user_and_profile()
        user.profile.counties.add(county)
        glean = create_glean(
            created_by=user,
            date=date.today() + timedelta(days=3),
            counties=county
        )
        announce = create_announcement(glean=glean)
        self.assertEqual(mail_from_source(announce), 0)

    def test_mail_from_source_testing_email(self):
        county = create_county()
        user = create_user_and_profile()
        user.profile.counties.add(county)
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
        user = create_user_and_profile()
        glean = create_glean(
            created_by=user,
            date=date.today() + timedelta(days=3),
            counties=county
        )
        announce = create_announcement(glean=glean)
        memo = announce.member_organization
        memo.testing = False
        memo.save()

        user = create_user_and_profile(tasks_gleaning=True)
        user.profile.counties.add(county)
        user = create_user_and_profile(tasks_gleaning=True)
        user.profile.counties.add(county)
        user = create_user_and_profile(tasks_gleaning=True)
        user.profile.counties.add(county)
        self.assertEqual(mail_from_source(announce), 3)


class AnnouncementViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        test_groups()

    def test_announcement_list_view(self):
        request = self.factory.get(reverse("announce:announcements"))
        request.user = create_user_and_profile()
        request.user.profile.member_organization = create_memorg()

        view = AnnouncementListView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

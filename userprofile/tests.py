"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User

from counties.models import County
from userprofile.models import Profile
from gleanevent.models import GleanEvent
from memberorgs.models import MemOrg


class ProfileModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        MemOrg.objects.create(name="Memo", pk=1)

    @classmethod
    def tearDownClass(cls):
        MemOrg.objects.get(pk=1).delete()

    def setUp(self):
        self.user = User.objects.create(
            username="volunteer",
            email="volunteer@example.com",
        )
        self.county = County.objects.create(name="County")
        self.profile = Profile.objects.create(user=self.user)
        self.profile.counties.add(self.county)
        self.memo = MemOrg.objects.get(pk=1)

    def test_notify_registration_method(self):
        self.memo.counties.add(self.county)
        notified = self.profile.notify_registration()
        self.assertTrue(
            self.memo in notified,
            "Notification System isn't working (simplest example)"
        )

    def test_notify_lead_organization(self):
        notified = self.profile.notify_registration()
        self.assertTrue(
            self.memo in notified,
            "Notification Failsafe didn't fire"
        )

    def test_notify_lead_organization_anyway(self):
        county_2 = County.objects.create(name="County2")
        memo_2 = MemOrg.objects.create(name="Memo2", pk=2)
        memo_2.counties.add(county_2)

        self.profile.counties.add(county_2)
        notified = self.profile.notify_registration()

        self.assertTrue(
            self.memo in notified,
            "Lead Organization not notified alongside others"
        )

    def test__unsubscribe_key(self):
        self.assertEqual(
            self.profile.unsubscribe_key,
            None,
            "Incorrect set up, should have empty profile to test"
        )
        self.assertTrue(
            self.profile._unsubscribe_key,
            "Private unsubscribe key method not corecing to true- "
            "probably not generating"
        )
        self.assertTrue(
            self.profile.unsubscribe_key,
            "Method did not save new unsubscirbe key to database."
        )

    def test_unsubscribe_url(self):
        unsub = self.profile.unsubscribe_url
        self.assertIn(
            "http://",
            unsub,
            "Unsubscribe URL not a URL: {0}".format(unsub)
        )
        self.assertIn(
            self.profile.unsubscribe_key,
            unsub,
            "Unsubscribe URL doesn't contain Unsub key: {0}".format(unsub)
        )

    def test_stock_unsubscribe_link(self):
        unsub = self.profile.stock_unsubscribe_link
        self.assertIn(
            "<a href='",
            unsub,
            "Stock Unsub contains no anchor tag: {0}".format(unsub)
        )

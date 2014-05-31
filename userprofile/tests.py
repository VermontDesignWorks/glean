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
        MemOrg.objects.create(name="Memo")

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
        memo_2 = MemOrg.objects.create(name="Memo2")
        memo_2.counties.add(county_2)

        self.profile.counties.add(county_2)
        notified = self.profile.notify_registration()

        self.assertTrue(
            self.memo in notified,
            "Lead Organization not notified alongside others"
        )

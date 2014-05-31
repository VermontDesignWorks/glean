from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import unittest

from memberorgs.models import MemOrg
from userprofile.models import Profile


class MemOrgModelTests(TestCase):

    def setUp(self):
        self.memo = MemOrg.objects.create(
            name="member organization 1",
            testing_email="memo@example.com",
            notify=True
        )

    def test_notify_admin_method_sends_mail(self):
        user = User.objects.create(username="test", email="user@example.com")
        profile = Profile.objects.create(user=user)
        result = self.memo.notify_admin(user)
        self.assertEqual(
            result,
            1,
            "Member Org notification logic didn't affirm it sent mail."
        )

    def test_notify_admin_method_sends_no_mail_if_notify_is_off(self):
        user = User.objects.create(username="test", email="user@example.com")
        profile = Profile.objects.create(user=user)
        self.memo.notify = False
        self.memo.save()
        result = self.memo.notify_admin(user)
        self.assertEqual(
            result,
            0,
            "Member Org notification logic didn't deny it sent mail"
        )

    def test_notify_admin_method_gracefully_fails_if_no_testing_email(self):
        user = User.objects.create(username="test", email="user@example.com")
        profile = Profile.objects.create(user=user)
        self.memo.testing_email = None
        self.memo.save()
        result = self.memo.notify_admin(user)
        self.assertEqual(
            result,
            0,
            "Member Org notificiation logic didn't deny it sent mail")

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import unittest

from announce.models import Template
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

    def test_create_default_template(self):
        template = self.memo.create_default_template()
        self.assertIsNotNone(
            template,
            "Default Template was not created via Memorg Model Method"
        )
        self.assertTrue(
            template.body,
            "Template seems to have rendered with an empty body"
        )

    def test_create_default_template_passes_if_default_exists(self):
        template = self.memo.create_default_template()
        second_default_template = self.memo.create_default_template()
        self.assertIsNone(second_default_template)

    def test_default_template_property_creates_new_templates(self):
        Template.objects.filter(member_organization=self.memo).delete()
        self.assertIsNotNone(self.memo.default_template)

    def test_default_template_property_fetches_existing_templates(self):
        template = Template.objects.create(
            member_organization=self.memo,
            default=True,
            template_name="test template"
        )
        self.assertEqual(template, self.memo.default_template)

    def test_default_template_property_fetches_only_one_template(self):
        template1 = Template.objects.create(
            member_organization=self.memo,
            default=True,
            template_name="test template"
        )
        template2 = Template.objects.create(
            member_organization=self.memo,
            default=True,
            template_name="test template 2"
        )
        self.assertIn(self.memo.default_template, [template1, template2])

from django.test import TestCase
from django.test.client import RequestFactory

from announce.models import Announcement

from test_functions import create_announcement

from .mixins import DateFilterMixin


class GenericMixinsTests(TestCase):
    def setUp(self):
        class BaseClass(object):
            def get_queryset(self):
                return Announcement.objects.all()
        self.BaseClass = BaseClass
        self.announcement = create_announcement()
        self.factory = RequestFactory()

    def test_date_filter_mixin(self):
        base = self.BaseClass()
        self.assertTrue(base.get_queryset().exists())

        class SubClass(DateFilterMixin, self.BaseClass):
            pass
        subclass = SubClass()
        subclass.request = self.factory.get(
            r"?date_from=06%2F10%2F2014&date_until=06%2F12%2F2014"
        )
        self.assertFalse(subclass.get_queryset().exists())

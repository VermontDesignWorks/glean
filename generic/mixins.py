import datetime
from datetime import date
import string

from django.core.paginator import Paginator
from django.utils.decorators import method_decorator, classonlymethod
from django.contrib.auth.decorators import login_required
import re


class SimpleLoginCheckForGenerics(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(
            SimpleLoginCheckForGenerics,
            self).dispatch(request, *args, **kwargs)


class DateFilterMixin(object):

    def get_queryset(self):
        get = self.request.GET
        queryset = super(DateFilterMixin, self).get_queryset()

        date_from_raw = get.get("date_from", '')
        if date_from_raw:
            date_from = datetime.datetime.strptime(date_from_raw, "%m/%d/%Y")
        else:
            date_from = datetime.date(2012, 01, 01)

        date_until_raw = get.get("date_until", '')
        if date_until_raw:
            date_until = datetime.datetime.strptime(date_until_raw, "%m/%d/%Y")
        else:
            date_until = datetime.date(2099, 01, 01)
        return queryset.filter(
            datetime__gte=date_from,
            datetime__lte=date_until
        )


class DynamicDateFilterMixin(object):
    'Dynamic Date Filter Mixin to return queryset by date for generic views'

    version = '0.2'
    # self.queryset must be set as base queryset to filter from
    # self.uniauth_string must be set to appropriate string to test uniauth rig

    def get_queryset(self):
        date_from = self.request.GET.get('date_from', '')
        date_until = self.request.GET.get('date_until', '')
        mo = self.request.user.profile.member_organization

        try:
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')

        except:
            try:
                date_from = datetime.datetime.strptime(date_from, '%m/%d/%Y')

            except:
                date_from = datetime.date(2000, 01, 01)

        try:
            date_until = datetime.datetime.strptime(date_until, '%Y-%m-%d')
        except:
            try:
                date_until = datetime.datetime.strptime(date_until, '%m/%d/%Y')
            except:
                date_until = datetime.datetime.now()
                date_until = date_until + datetime.timedelta(days=3650)
                date_until = datetime.date(
                    date_until.year, date_until.month, date_until.day)

        queryset = self.queryset.filter(
            date__gte=date_from,
            date__lte=date_until
        ).order_by("-date")
        if not self.request.user.has_perm(permission):
            queryset = queryset.filter(
                date__gte=date_from,
                date__lte=date_until,
                member_organization=mo
            )
        if queryset.count() > 40:
            queryset = queryset[:40]
        permission = self.uniauth_string
        return queryset

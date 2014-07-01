import datetime

from django.utils.decorators import method_decorator, classonlymethod
from django.contrib.auth.decorators import login_required


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
    'Dynamic Date Filter Mixin requires self.queryset to be set as a base queryset to extract from'

    def get_queryset(self):
        queryset = self.queryset
        date_from = self.request.GET.get('date_from', '')
        date_until = self.request.GET.get('date_until', '')
        mo = self.request.user.profile.member_organization
        date_from_test = date_from
        date_until_test = date_until
        dateparts_from = date_from.split('-')
        dateparts_until = date_until.split('-')
        dateparts_today = ["a", "a", "a"]
        dateparts_slash_from = date_from_test.split('/')
        dateparts_slash_until = date_until_test.split('/')

        try:
            date_from_test = datetime.date(int(dateparts_from[0]), int(dateparts_from[1]), int(dateparts_from[2]))
        except:
            try:
                date_from_test = datetime.date(int(dateparts_slash_from[2]), int(dateparts_slash_from[0]), int(dateparts_slash_from[1]))
                date_from = dateparts_slash_from[2]+'-'+dateparts_slash_from[0]+'-'+dateparts_slash_from[1]
            except:
                import sys
                print >> sys.stderr, "default"
                date_from = '2000-01-01'

        try:
            date_until_test = datetime.date(int(dateparts_until[0]), int(dateparts_until[1]), int(dateparts_until[2]))
        except:
            try:
                date_until_test = datetime.date(int(dateparts_slash_until[2]), int(dateparts_slash_until[0]), int(dateparts_slash_until[1]))
                date_until = dateparts_slash_until[2]+'-'+dateparts_slash_until[0]+'-'+dateparts_slash_until[1]
            except:
                import sys
                print >> sys.stderr, "default"
                dateparts_today[0] = str(datetime.date.today().year)
                dateparts_today[1] = str(datetime.date.today().month)
                dateparts_today[2] = str(datetime.date.today().day)
                date_until = dateparts_today[0]+'-'+dateparts_today[1]+'-'+dateparts_today[2]

        queryset = self.queryset.filter(
            date__gte=date_from,
            date__lte=date_until
        )

        if not self.request.user.has_perm('distro.uniauth'):
            queryset = queryset.filter(
                date__gte=date_from,
                date__lte=date_until,
                member_organization=mo
            )
            
        return queryset
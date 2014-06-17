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

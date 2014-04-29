import datetime


class DateFilterMixin(object):

    @property
    def from_date(self):
        try:
            return datetime.datetime.strptime(
                self.request.GET["date_until"],
                "%m/%d/%Y").date()
        except:
            return False

    @property
    def until_date(self):
        try:
            return datetime.datetime.strptime(
                self.request.GET["date_until"],
                "%m/%d/%Y").date()
        except:
            return False

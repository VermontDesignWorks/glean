from django.utils.decorators import method_decorator, classonlymethod
from django.contrib.auth.decorators import login_required


class SimpleLoginCheckForGenerics(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SimpleLoginCheckForGenerics, self).dispatch(*args, **kwargs)
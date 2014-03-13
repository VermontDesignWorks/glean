import datetime
import time
from django.utils import timezone

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from userprofile.models import Profile
from gleanevent.models import GleanEvent
from django.contrib.sites.models import Site
from posts.models import Post

from memberorgs.models import MemOrg

from constants import DAYS


def home(request):
    if request.user.is_anonymous():
        return render(request, 'anon_home.html', {})
    todays_gleans = GleanEvent.objects.filter(date=datetime.date.today())
    l = []
    today = datetime.date.today()
    predate = (datetime.date.today().weekday() + 1) % 7

    for i in range(-predate, 14-predate):
        query = GleanEvent.objects.filter(
            date=today+datetime.timedelta(days=i))
        more = False
        if query.count() > 9:
            query = query[:9]
            more = True
        l.append([
            timezone.now()+datetime.timedelta(days=i),
            query,
            more,
            i])
    posts = Post.objects.order_by('datetime')[:10]
    days = l
    two_weeks = datetime.date.today()+datetime.timedelta(days=14)
    future = GleanEvent.objects.filter(date__gte=two_weeks)

    days = l
    memberorgs = MemOrg.objects.all()

    ## BETA CODE
    profile = request.user.profile_set.get()
    not_notified = getattr(profile, "not_notified", False)
    profile.not_notified = False
    profile.save()
    ## BETA CODE

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'days': days,
            'future': future,
            'two_weeks': two_weeks,
            'memberorgs': memberorgs,
            'not_notified': not_notified,
        }
    )

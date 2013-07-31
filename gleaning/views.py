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
	if not request.user.is_anonymous() and not Profile.objects.filter(user=request.user).exists():
		return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
	todays_gleans = GleanEvent.objects.filter(date=datetime.date.today())
	l = []
	today = datetime.date.today()
	for i in range(14):
		query = GleanEvent.objects.filter(date=today+datetime.timedelta(days=i))
		more = False
		if query.count() > 9:
			query = query[:9]
			more = True
		l.append([timezone.now()+datetime.timedelta(days=i),
			query,
			more
			])
	posts = Post.objects.order_by('datetime')[:10]
	days = l
	two_weeks = datetime.date.today()+datetime.timedelta(days=14)
	future = GleanEvent.objects.filter(date__gte=two_weeks)

	days = l
	memberorgs = MemOrg.objects.all()
	return render(request, 'home.html', {'posts':posts, 'days':days, 'future':future, 'two_weeks':two_weeks, 'memberorgs':memberorgs})

	# try:
	# 	prof = Profile.objects.get(user=request.user)
	# 	lastday = datetime.datetime.now()+datetime.timedelta(days=7)
	# 	day1 = datetime.datetime.now()
	# 	gleans = list(GleanEvent.objects.filter(date__gte=day1,date__lte=lastday))
	# 	return render(request, 'home.html',{'gleans' : gleans})
	# except:
	# 	if not request.user.is_anonymous():
	# 		return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
	# 	else:
	# 		lastday = datetime.datetime.now()+datetime.timedelta(days=7)
	# 		day1 = datetime.datetime.now()
	#         gleans = list(GleanEvent.objects.filter(date__gte=day1,date__lte=lastday))
	#         return render(request, 'home.html',{'gleans' : gleans})

	

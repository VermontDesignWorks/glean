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

from constants import DAYS
todays_gleans = GleanEvent.objects.filter(date=datetime.date.today())
l = []
today = datetime.date.today()
for i in range(len(DAYS)):
	debug = timezone.now()+datetime.timedelta(days=i)
	l.append([debug.strftime('%A') + ' ' + debug.strftime('%d'),
		GleanEvent.objects.filter(date=datetime.timedelta(days=i)+today)
		])

def home(request):
	if not request.user.is_anonymous() and not Profile.objects.filter(user=request.user).exists():
		return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
	posts = Post.objects.order_by('datetime')[:10]
	days = l
	future = GleanEvent.objects.filter(date__gte=datetime.date.today()+datetime.timedelta(days=7),date__lte=datetime.date.today()+datetime.timedelta(days=14))
	#debug2 = (debug + datetime.timedelta(days=1)).strftime('%d')
	days = l
	#debug2 = (debug + datetime.timedelta(days=1)).strftime('%d')
	return render(request, 'home.html', {'posts':posts, 'days':days, 'future':future})

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

	

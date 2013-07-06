import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from gleanevent import models
#<<<<<<< HEAD
from gleanevent.models import models
#=======
from userprofile.models import Profile
from gleanevent.models import GleanEvent
#>>>>>>> Tim

def home(request):
	try:
		prof = Profile.objects.get(user=request.user)
	except:
		if not request.user.is_anonymous():
			return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
		else:
			lastday = datetime.datetime.now()+datetime.timedelta(days=7)
			day1 = datetime.datetime.now()
	        gleans = list(GleanEvent.objects.filter(date__gte=day1,date__lte=lastday))
	        return render(request, 'home.html',{'gleans' : gleans})
	

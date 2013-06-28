from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from gleanevent import models

def home(request):
	from userprofile.models import Profile
	try:
		prof = Profile.objects.get(user=request.user)
	except:
		if not request.user.is_anonymous():
			return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
		else:
			return render(request, 'home.html', {'debug':str(request.user.is_anonymous())})
	return render(request, 'home.html', {'debug':str(prof)})

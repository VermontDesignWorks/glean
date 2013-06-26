from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import user_passes_test
from gleanevent import models

#def extremes(user):
#	return user.username == 'AnonymousUser' or user.reverse_to_userprofile.detailed()

#@user_passes_test(extremes)
def home(request):
	return render(request, 'home.html')
# Create your views here.
import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from django.contrib.auth.decorators import permission_required

def index(request):
	return HttpResponseRedirect(reverse('home'))
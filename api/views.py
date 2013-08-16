# Create your views here.

import time
import datetime
import random
import json

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
from django.core import serializers

from django.views import generic
from django import forms
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


from farms.models import Farm, FarmLocation

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from functions import primary_source


#==================== Farm Ajax Query System ====================#

#== Farm API ==#
def apiFarm(request, farm_id):
	farm = get_object_or_404(Farm, name=farm_id)
	data = serializers.serialize('json', Farm.objects.filter(name=farm_id), fields=('directions', 'instructions'))
	farm_location = serializers.serialize('json', FarmLocation.objects.filter(farm=farm), fields=('name'))
#	data += farm_location
	return HttpResponse(data[1:-1])

#== Farm Location API==#
def apiFarmLocation(request, farm_location_id):
	farm_location = get_object_or_404(FarmLocation, pk=farm_location_id)
	return HttpResponse(farm_location)
		
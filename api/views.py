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
from django.utils import simplejson as json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


from farms.models import Farm, FarmLocation
from memberorgs.models import MemOrg

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from functions import primary_source


#==================== Farm Ajax Query System ====================#

#== Farm API ==#
def apiFarm(request, farm_id):
	farm = get_object_or_404(Farm, name=farm_id)
	farm_locations = FarmLocation.objects.filter(farm=farm)
	data = {
		'instructions':farm.instructions,
		'directions':farm.directions, 
		'address_one':farm.address_one,
		'address_two':farm.address_two,
		'city':farm.city,
		'state':farm.state,
		'zipcode':farm.zipcode,
		'counties':[],
		'farm_locations':{'':"---------"},
	}
	for county in farm.counties.all():
		data['counties'].append(county.id)
	for location in farm_locations:
		data['farm_locations'][location.id] = [location.name]
	return HttpResponse(json.dumps(data), mimetype="application/json")

#== Farm Location API==#
def apiFarmLocation(request, farm_id, farm_location_id):
	farm = get_object_or_404(Farm, name=farm_id)
	farm_location = get_object_or_404(FarmLocation, name=farm_location_id)
	data = {'instructions':farm_location.instructions,
		'directions':farm_location.directions, 
		'address_one':farm_location.address_one,
		'address_two':farm_location.address_two,
		'city':farm_location.city,
		'state':farm_location.state,
		'zipcode':farm_location.zipcode,
		'counties':[]
	}
	for county in farm_location.counties.all().order_by("-name"):
		data['counties'].append(county.id)
	return HttpResponse(json.dumps(data), mimetype="application/json")
		
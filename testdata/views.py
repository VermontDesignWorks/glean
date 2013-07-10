# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm, EmailForm
from counties.models import County
from constants import VERMONT_COUNTIES, FARM_TYPE

import random
from userprofile.models import Profile
from announce.models import Template

from farms.models import Farm, FarmLocation

county_quant = 7
user_quant = 20
template_quant = 1
farm_quant = 7
loc_divinto_farms = 15

def index(request):
	if County.objects.filter(name='County1').exists():
		return HttpResponse("<a href='/'>Go home.</a>")
	for i in range(county_quant):
		new = County(name="County"+str(i),description="County"+str(i), towns="Town"+str(i))
		new.save()
	for i in range(user_quant):
		name = 'name' + str(i)
		person = User.objects.create_user(name, 'Cheekio@gmail.com', '463597')
		userprof = Profile(user=person, first_name = 'firsty'+str(i),last_name='lasty'+str(i))
		userprof.save()
		choices = range(county_quant)
		choice1 = choices.pop(random.choice(choices))
		county = County.objects.get(name='County'+str(choice1))
		
		userprof.counties.add(county)
		userprof.save()
	for i in range(template_quant):
		new = Template(template_name="template"+str(1), body="{{content}}{{glean.title}}{{glean.description}}{{rsvp}}{{info}}{{unsubscribe}}")
		new.save()
	my_user = 0
	my_county = 0
	for i in range(farm_quant):
		if my_user >= user_quant:
			my_user = 0
		if my_county >= county_quant:
			my_county = 0
		new = Farm(name="farm"+str(i),farm_type=FARM_TYPE[0][1],description="generic farm",physical_address_one="36 maple street",physical_city="Morrisville",physical_state="VT",physical_is_mailing=True,phone_1='8025786266',email="Joshua.Lucier@gmail.com",direction="Many different directions",instructions="many instructions")
		new.save()
		new.farmers.add(User.objects.all()[my_user])
		new.counties.add(County.objects.all()[my_county])
		my_user = my_user + 1
		my_county = my_county + 1
	my_farm = 0
	my_county = 0
	for i in range(loc_divinto_farms):
		if my_farm >= farm_quant:
			my_farm = 0
		if my_county >= county_quant:
			my_county = 0
		new = FarmLocation(farm=Farm.objects.all()[my_farm],name="location"+str(i),description="Grand Central Field",directions="all kinds of directions")
		new.save()
		new.counties.add(County.objects.all()[my_county])
		my_farm = my_farm + 1
		my_county = my_county + 1
	return HttpResponse("Your data has been created. <a href='/'>Go home.</a>")


# class Template(models.Model):
# 	template_name = models.CharField(max_length=40, unique=True)
# 	#member_organization = models.ManyToManyField(Group, editable=False, blank=True, null=True)
# 	body = models.TextField()
# 	def __unicode__(self):
# 		return self.template_name# sel
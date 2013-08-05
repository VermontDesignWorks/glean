# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm, EmailForm
from counties.models import County
from constants import VERMONT_COUNTIES, FARM_TYPE

import random
from userprofile.models import Profile
from announce.models import Template

from farms.models import Farm, FarmLocation, Contact
from memberorgs.models import MemOrg
from recipientsite.models import RecipientSite
from announce.models import Announcement
from distro.models import Distro
from gleanevent.models import GleanEvent, PostGlean
from posts.models import Post

county_quant = 7
user_quant = 20
template_quant = 1
farm_quant = 7
loc_divinto_farms = 15
memberorg_quant = 3
recipient_sites = 3

def delete(request):
	for announce in Announcement.objects.all():
		announce.delete()

# def groupsAndPerms(request):
# 	# if not Group.objects.all():
# 	# 	vol = Group(name="Volunteer")
# 	# 	vol.save()
# 	# 	ed = Group(name="Member Organization Executive Director")
# 	# 	ed.save()
# 	# 	mc = Group(name="Member Organization Glean Coordinator")
# 	# 	mc.save()
# 	# 	sal = Group(name="Salvation Farms Administrator")
# 	# 	sal.save()
# 	# 	salc = Group(name="Salvation Farms Coordinator")
# 	# 	salc.save()


# 	# ed = Group.objects.get(name="Member Organization Executive Director")
# 	# if not ed.permissions.all():
		

# 	# 	mo_list = [Announcement, Template, Distro, GleanEvent, Farm, PostGlean, RecipientSite, Profile, MemOrg, Post]
# 	# 	uni_list = [Announcement, Template, Distro, GleanEvent, Farm, FarmLocation, Contact, PostGlean, RecipientSite, Profile, MemOrg, County, Post]

# 	# 	modelc = Group.objects.get(name="Member Organization Glean Coordinator")
# 	# 	sal = Group.objects.get(name="Salvation Farms Administrator")
# 	# 	salc = Group.objects.get(name="Salvation Farms Coordinator")

# 	# 	for model in mo_list:
# 	# 		content_type = ContentType.objects.get_for_model(model)
# 	# 		perm = Permission.objects.get(codename='auth', content_type=content_type)
# 	# 		ed.permissions.add(perm)
# 	# 		mc.permissions.add(perm)
# 	# 		sal.permissions.add(perm)
# 	# 		salc.permissions.add(perm)
# 	# 	for model in uni_list:
# 	# 		content_type = ContentType.objects.get_for_model(model)
# 	# 		perm = Permission.objects.get(codename='uniauth', content_type=content_type)
# 	# 		sal.permissions.add(perm)
# 	# 		salc.permissions.add(perm)
		
# 	# 	# for model in mo_list:
# 	# 	# 	ed.permissions.add(model.moauth)


# 	# 	# for model in uni_list:
# 	# 	# 	content_type = ContentType.objects.get_for_model(model)
# 	# 	# 	moauth = Permission.objects.create(	codename="uniauth",
# 	# 	# 										name="Universal Authorization and Permissions",
# 	# 	# 										content_type=content_type)
		
		
# 	# 	return HttpResponse("perms and users are made")
# 	# else:
# 	# 	return HttpResponse("perms and users are already made")


def index(request):

	

	#return HttpResponse('worked')
	if not Group.objects.all():
		vol = Group(name="Volunteer")
		vol.save()
		ed = Group(name="Member Organization Executive Director")
		ed.save()
		mc = Group(name="Member Organization Glean Coordinator")
		mc.save()
		sal = Group(name="Salvation Farms Administrator")
		sal.save()
		salc = Group(name="Salvation Farms Coordinator")
		salc.save()


	ed = Group.objects.get(name="Member Organization Executive Director")
	if not ed.permissions.all():
		

		mo_list = [Announcement, Template, Distro, GleanEvent, Farm, PostGlean, RecipientSite, Profile, MemOrg, Post]
		uni_list = [Announcement, Template, Distro, GleanEvent, Farm, FarmLocation, Contact, PostGlean, RecipientSite, Profile, MemOrg, County, Post]

		mc = Group.objects.get(name="Member Organization Glean Coordinator")
		sal = Group.objects.get(name="Salvation Farms Administrator")
		salc = Group.objects.get(name="Salvation Farms Coordinator")

		for model in mo_list:
			content_type = ContentType.objects.get_for_model(model)
			perm = Permission.objects.get(codename='auth', content_type=content_type)
			ed.permissions.add(perm)
			mc.permissions.add(perm)
			sal.permissions.add(perm)
			salc.permissions.add(perm)
		for model in uni_list:
			content_type = ContentType.objects.get_for_model(model)
			perm = Permission.objects.get(codename='uniauth', content_type=content_type)
			sal.permissions.add(perm)
			salc.permissions.add(perm)

	


	if County.objects.filter(name='County1').exists():
		return HttpResponse("<a href='/'>Go home.</a>")
	for i in range(memberorg_quant):
		new = MemOrg(name="MemberOrg"+str(i), description="This is the "+str(i)+"th member org in our gleaning collective!", counties = "A bunch of counties are covered by us, including {insert counties here}")
		new.save()
		newTemp = Template(template_name="Default template", body="<html><body>{{content}}{{glean.title}}{{glean.description}}{{rsvp}}{{info}}{{unsubscribe}}</body></html>", member_organization=new)
		newTemp.save()
	for i in range(recipient_sites):
		choices2 = range(memberorg_quant)
		choice2 = choices2.pop(random.choice(choices2))
		memorg = MemOrg.objects.get(name="MemberOrg"+str(choice2))
		new = RecipientSite(name="RecipientSite" + str(i), address_one = "515 Main Street", city="Morrisville", state="VT", zipcode="01771",member_organization=memorg)
		new.save()
	for i in range(county_quant):
		new = County(name="County"+str(i),description="County"+str(i), towns="Town"+str(i))
		new.save()
	for i in range(user_quant):
		name = 'name' + str(i)
		choices2 = range(memberorg_quant)
		choice2 = choices2.pop(random.choice(choices2))
		memorg = MemOrg.objects.get(name="MemberOrg"+str(choice2))
		person = User.objects.create_user(name, 'Cheekio@gmail.com', 'password')
		if name == "name0":
			vol = Group.objects.get(name="Salvation Farms Administrator")
			person.groups.add(vol)
			vol = None
		elif name == "name1":
			vol = Group.objects.get(name="Member Organization Executive Director")
			person.groups.add(vol)
			vol = None
		else:
			vol = Group.objects.get(name="Volunteer")
			person.groups.add(vol)
			vol = None
		userprof = Profile(user=person, first_name = 'firsty'+str(i),last_name='lasty'+str(i), member_organization=memorg)
		userprof.save()
		choices = range(county_quant)
		choice1 = choices.pop(random.choice(choices))
		county = County.objects.get(name='County'+str(choice1))
		userprof.counties.add(county)
		userprof.save()
	my_user = 0
	my_county = 0
	for i in range(farm_quant):
		if my_user >= user_quant:
			my_user = 0
		if my_county >= county_quant:
			my_county = 0
		choices2 = range(memberorg_quant)
		choice2 = choices2.pop(random.choice(choices2))
		memorg = MemOrg.objects.get(name="MemberOrg"+str(choice2))
		new = Farm(name="farm"+str(i),farm_type=FARM_TYPE[0][1],address_one="100 Main Street",address_two="apartment 3",city="Burlington",state="VT",description="generic farm",physical_is_mailing=True,phone_1='8025786266',email="Joshua.Lucier@gmail.com",direction="Many different directions",instructions="many instructions")
		new.save()
		new.member_organization.add(memorg)
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

def accounts(request):
	#person = User.objects.create_user('Vista@Salvation', 'vista@salvation.org', 'password')
	#person.save()
	person = User.objects.get(username='Vista@Salvation')
	vol = Group.objects.get(name="Salvation Farms Administrator")
	person.groups.add(vol)
	memorg = MemOrg.objects.get(name="MemberOrg0")
	userprof = Profile(user=person, first_name = 'Marcella', last_name="Houghton", member_organization=memorg)
	userprof.save()
	counties = County.objects.all()
	for county in counties:
		userprof.counties.add(county)
	return HttpResponse('that all worked')

# class Template(models.Model):
# 	template_name = models.CharField(max_length=40, unique=True)
# 	#member_organization = models.ManyToManyField(Group, editable=False, blank=True, null=True)
# 	body = models.TextField()
# 	def __unicode__(self):
# 		return self.template_name# sel

def accounts(request):
	return HttpResponseRedirect(reverse('home'))
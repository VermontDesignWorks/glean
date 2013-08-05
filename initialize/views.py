from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from userprofile.models import Profile
from announce.models import Template
from farms.models import Farm, FarmLocation, Contact
from memberorgs.models import MemOrg
from recipientsite.models import RecipientSite
from announce.models import Announcement
from distro.models import Distro
from gleanevent.models import GleanEvent, PostGlean
from posts.models import Post
from django.contrib.auth.models import Group

# Create your views here.


def create(request):
	if not request.user.is_superuser and Group.objects.all():
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
	else:
		return HttpResponseRedirect(reverse('home'))

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
	return HttpResponseRedirect(reverse('home'))
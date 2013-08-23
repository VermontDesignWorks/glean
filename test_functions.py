import random
from django.contrib.auth.models import User
from userprofile.models import Profile
from gleanevent.models import GleanEvent, PostGlean
from memberorgs.models import MemOrg
from announce.models import Announcement
from counties.models import County


def create_volunteer_user_object():
	alphabet = 'the quick brown fox jumps over a lazy dog'
	name = ''
	for i in range(12):
		name += random.choice(alphabet)
	return User.objects.create_user(name,name+"@example.com","password")

def create_profile(user, **kwargs):
	profile = Profile(user=user, first_name="John", last_name="Doe", **kwargs)
	profile.save()
	return profile

def create_user_and_profile(**kwargs):
	user = create_volunteer_user_object()
	return user, create_profile(user, **kwargs)

def create_county():
	county = County(name="TestCounty")
	county.save()
	return county

def create_post_glean(glean, **kwargs):
	pg = PostGlean(glean=glean, **kwargs)
	pg.save()
	return pg

def create_memorg():
	memorg = MemOrg(name="Test Member Organization")
	memorg.save()
	return memorg

def create_glean(**kwargs):
	memorg = create_memorg()
	if 'created_by' in kwargs:
		glean = GleanEvent(
						member_organization=memorg,
						**kwargs)
	else:
		glean = GleanEvent(created_by=create_volunteer_user_object(),
						member_organization=memorg,
						**kwargs)
	glean.save()
	return glean

def create_announcement(**kwargs):
	if 'glean' in kwargs and 'member_organization' in kwargs:
		announce = Announcement(**kwargs)
	elif 'glean' in kwargs:
		memorg = create_memorg
		announce = Announcement(member_organization=memorg, **kwargs)
	elif 'member_organization' in kwargs:
		glean = create_glean
		announce = Announcement(glean=glean, **kwargs)
	else:
		glean = create_glean()
		memorg = create_memorg()
		announce = Announcement(glean=glean, member_organization=memorg, **kwargs)
	announce.save()
	return announce
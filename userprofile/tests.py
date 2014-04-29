"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.contrib.auth.models import User
from userprofile.models import Profile
from gleanevent.models import GleanEvent, PostGlean
from memberorgs.models import MemOrg


def create_volunteer_user_object():
    return User.objects.create_user(
        "TestUser",
        "TestUser@example.com",
        "password")


def create_profile(user):
    profile = Profile(
        user=user,
        first_name="John",
        last_name="Doe",
        waiver=True,
        agreement=True,
        photo_release=False)
    profile.save()
    return profile


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
        glean = GleanEvent(
            created_by=create_volunteer_user_object(),
            member_organization=memorg,
            **kwargs)
    glean.save()
    return glean

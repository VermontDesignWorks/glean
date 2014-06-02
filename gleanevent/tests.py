"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from gleanevent.models import GleanEvent
from userprofile.models import Profile
from memberorgs.models import MemOrg
from farms.models import Farm, FarmLocation


def create_volunteer_user_object():
    return User.objects.create_user(
        "TestUser", "TestUser@example.com", "password")


def create_profile(user, memorg):
    profile = Profile(
        user=user,
        first_name="John",
        last_name="Doe",
        member_organization=memorg,
        waiver=True,
        agreement=True
    )
    profile.save()
    return profile


def create_memorg():
    memorg = MemOrg(name="Test Member Organization")
    memorg.save()
    return memorg


def create_glean(**kwargs):
    memorg = create_memorg()
    if 'created_by' in kwargs:
        glean = GleanEvent(member_organization=memorg, **kwargs)
    else:
        glean = GleanEvent(
            created_by=create_volunteer_user_object(),
            member_organization=memorg,
            **kwargs)
    glean.save()
    return glean


def create_farm(**kwargs):
    farm = Farm(name="TestFarm", **kwargs)
    farm.save()
    return farm


def create_farm_location(farm, **kwargs):
    farmlocation = FarmLocation(farm=farm, **kwargs)
    farmlocation.save()
    return farmlocation


class GleanEventTests(TestCase):
    def test_happened(self):
        now = timezone.now().date()
        upcomming_glean = create_glean(
            date=now + datetime.timedelta(days=5))
        upcomming_glean.save()
        self.assertEqual(upcomming_glean.happened(), False)

    def test_render_directions(self):
        user = create_volunteer_user_object()
        glean = create_glean(created_by=user)
        self.assertTrue(glean.render_directions())

        farm = create_farm()
        glean = create_glean(farm=farm, created_by=user)
        self.assertTrue(glean.render_directions())

        farm = create_farm(directions="Farm Directions")
        glean = create_glean(farm=farm, created_by=user)
        self.assertEqual(glean.render_directions(), farm.directions)

        farm = create_farm()
        farm_location = create_farm_location(farm=farm)
        glean = create_glean(
            farm=farm, farm_location=farm_location, created_by=user)
        self.assertTrue(glean.render_directions())

        farm_location = create_farm_location(
            farm=farm, directions="Farm Location Directions")
        glean = create_glean(
            farm=farm, farm_location=farm_location, created_by=user)
        self.assertEqual(glean.render_directions(), farm_location.directions)

        farm_location = create_farm_location(
            farm=farm, directions="Farm Location Directions")
        glean = create_glean(
            farm=farm,
            farm_location=farm_location,
            created_by=user,
            directions="Glean Directions")
        self.assertEqual(glean.render_directions(), glean.directions)

        farm = create_farm(directions="Farm Directions")
        glean = create_glean(
            farm=farm, created_by=user, directions="Glean Directions")
        self.assertEqual(glean.render_directions(), glean.directions)

        glean = create_glean(created_by=user, directions="Glean Directions")
        self.assertEqual(glean.render_directions(), glean.directions)

    def test_render_instructions(self):
        user = create_volunteer_user_object()
        glean = create_glean(created_by=user)
        self.assertEqual(
            glean.render_instructions(), u"Show up early and have fun!")

        farm = create_farm()
        glean = create_glean(farm=farm, created_by=user)
        self.assertEqual(
            glean.render_instructions(), u"Show up early and have fun!")

        farm = create_farm(instructions="Farm instructions")
        glean = create_glean(farm=farm, created_by=user)
        self.assertEqual(glean.render_instructions(), farm.instructions)

        farm = create_farm()
        farm_location = create_farm_location(farm=farm)
        glean = create_glean(
            farm=farm, farm_location=farm_location, created_by=user)
        self.assertEqual(
            glean.render_instructions(), u"Show up early and have fun!")

        farm_location = create_farm_location(
            farm=farm, instructions="Farm Location instructions")
        glean = create_glean(
            farm=farm, farm_location=farm_location, created_by=user)
        self.assertEqual(
            glean.render_instructions(), farm_location.instructions)

        farm_location = create_farm_location(
            farm=farm, instructions="Farm Location instructions")
        glean = create_glean(
            farm=farm,
            farm_location=farm_location,
            created_by=user,
            instructions="Glean instructions")
        self.assertEqual(glean.render_instructions(), glean.instructions)

        farm = create_farm(instructions="Farm instructions")
        glean = create_glean(
            farm=farm, created_by=user, instructions="Glean instructions")
        self.assertEqual(glean.render_instructions(), glean.instructions)

        glean = create_glean(
            created_by=user, instructions="Glean instructions")
        self.assertEqual(glean.render_instructions(), glean.instructions)


class GleanEventModelTests(TestCase):
    def setUp(self):
        self.glean = create_glean()

    def test_glean_url(self):
        self.assertIn(
            "http://",
            self.glean.url,
            "Glean URL doesn't contain HTTP:{0}".format(self.glean.url)
        )

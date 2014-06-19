import random
from django.contrib.auth.models import User, Group, Permission
from userprofile.models import Profile
from gleanevent.models import GleanEvent
from memberorgs.models import MemOrg
from announce.models import Announcement
from counties.models import County
<<<<<<< HEAD
from farms.models import Farm, FarmLocation
=======
from farms.models import Farm
from announce.models import Template
>>>>>>> master


class test_groups(object):
    'An object containing the five groups in the database and their permissions for testing'
    def __init__(self):
        self.volunteer = Group.objects.create(name="Volunteer")
        self.Member_Organization_Executive_Director = Group.objects.create(name="Member Organization Executive Director")
        self.Member_Organization_Glean_Coordinator = Group.objects.create(name="Member Organization Glean Coordinator")
        self.Salvation_Farms_Administrator = Group.objects.create(name="Salvation Farms Administrator")
        self.Salvation_Farms_Coordinator = Group.objects.create(name="Salvation Farms Coordinator")
        auth = Permission.objects.filter(codename="auth").all()
        for permission in auth:
            self.Member_Organization_Glean_Coordinator.permissions.add(permission)
            self.Member_Organization_Executive_Director.permissions.add(permission)
            self.Salvation_Farms_Administrator.permissions.add(permission)
            self.Salvation_Farms_Coordinator.permissions.add(permission)
        promote = Permission.objects.filter(codename="promote").all()
        for permission in promote:
            self.Member_Organization_Executive_Director.permissions.add(permission)
            self.Salvation_Farms_Administrator.permissions.add(permission)
            self.Salvation_Farms_Coordinator.permissions.add(permission)
        uniauth = Permission.objects.filter(codename="uniauth").all()
        for permission in uniauth:
            self.Salvation_Farms_Coordinator.permissions.add(permission)
            self.Salvation_Farms_Administrator.permissions.add(permission)
        self.volunteer.save()
        self.Member_Organization_Glean_Coordinator.save()
        self.Member_Organization_Executive_Director.save()
        self.Salvation_Farms_Coordinator.save()
        self.Salvation_Farms_Administrator.save()


def create_volunteer_user_object():
    alphabet = 'the quick brown fox jumps over a lazy dog'
    name = ''
    for i in range(12):
        name += random.choice(alphabet)
    return User.objects.create_user(name, name+"@example.com", "password")


def create_profile(user, **kwargs):
    profile = Profile(
        user=user,
        first_name="John",
        last_name="Doe",
        waiver=True,
        agreement=True,
        photo_release=False,
        **kwargs)
    profile.save()
    return profile


def create_salvation_farms_admin(salfarmgroup, memberorg):
    user = User.objects.create_user("salfarmadmin", "salfarmadmin@gmail.com", "password")
    user.is_staff = True
    user.is_superuser = True
    user.groups.add(salfarmgroup)
    user.save()
    profile = create_profile(user)
    user.profile.member_organization = memberorg
    user.profile.save()
    return user


def create_special_user(thegroup, memberorg):
    user = User.objects.create_user("specialuser", "specialuser@gmail.com", "password")
    user.groups.add(thegroup)
    user.save
    profile = create_profile(user)
    user.profile.member_organization = memberorg
    user.profile.save()
    return user


def create_user_and_profile(**kwargs):
    user = create_volunteer_user_object()
    create_profile(user, **kwargs)
    user.save()
    user.profile.save()
    return user


def create_county(**kwargs):
    county = County.objects.create(name="TestCounty")
    county.save()
    return county


def create_memorg(**kwargs):
    memorg = MemOrg.objects.create(name="Test Member Organization", **kwargs)
    memorg.save()
    return memorg


def create_farm(memberorg, **kwargs):
    farm = Farm.objects.create(name="Test Farm", **kwargs)
    farm.member_organization.add(memberorg)
    farm.save()
    return farm


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


def create_announcement(**kwargs):
    if 'glean' in kwargs and 'member_organization' in kwargs:
        announce = Announcement(**kwargs)
    elif 'glean' in kwargs:
        memorg = create_memorg()
        announce = Announcement(member_organization=memorg, **kwargs)
    elif 'member_organization' in kwargs:
        glean = create_glean()
        announce = Announcement(glean=glean, **kwargs)
    else:
        glean = create_glean()
        memorg = create_memorg()
        announce = Announcement(
            glean=glean, member_organization=memorg, **kwargs)
    announce.save()
    return announce


<<<<<<< HEAD
def create_location(farm, **kwargs):
    location = FarmLocation.objects.create(name="Test Location", **kwargs)
    location.farm = farm
    location.save()
    return location
=======
def create_template(memorg, **kwargs):
    template = Template.objects.create(template_name="Test Template", member_organization=memorg, **kwargs)
    template.save()
    return template
>>>>>>> master

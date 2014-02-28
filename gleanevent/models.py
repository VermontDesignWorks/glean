import datetime

from django.db import models
from django.forms import TextInput
from django.forms import ModelForm

from constants import STATES, TIME_OF_DAY

from django.contrib.auth.models import User
from farms.models import Farm, FarmLocation
from memberorgs.models import MemOrg
from counties.models import County

# Create your models here.

class GleanEvent(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField('Date', blank=True, null=True)
    time = models.CharField('Time', max_length=40, blank=True, null=True)
    time_of_day = models.CharField('General Time of Day', choices=TIME_OF_DAY, max_length=2, default="NA")
    farm = models.ForeignKey(Farm, blank=True, null=True)
    farm_location = models.ForeignKey(FarmLocation, blank=True, null=True)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True, null=True)
    volunteers_needed = models.IntegerField(blank = True, default=1)
    duration = models.CharField(max_length=30, blank=True, null=True)

    address_one = models.CharField('Address (line one)', max_length=200, blank=True)
    address_two = models.CharField('Address (line two)',max_length=200, blank=True)
    city = models.CharField('Address (City)', max_length=200, blank=True)
    state = models.CharField("State",choices=STATES, default="VT", max_length=2, blank=True)
    zipcode = models.CharField('Address Zip Code', max_length=11, blank=True)

    directions = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, editable=False, related_name="created_by")
    invited_volunteers = models.ManyToManyField(User, null=True, blank=True, related_name="invited_volunteers")

    rsvped = models.ManyToManyField(User, null=True, blank=True, related_name ="rsvped", editable=False)
    not_rsvped = models.ManyToManyField(User, null=True, blank=True, related_name ="not_rsvped", editable=False)
    waitlist = models.ManyToManyField(User, null=True, blank=True, related_name="waitlisted", editable=False)

    attending_volunteers = models.ManyToManyField(User, null=True, blank=True, related_name="attending_voluntters")
    officiated_by = models.ManyToManyField(User, blank=True, related_name="officiated_by")
    counties = models.ManyToManyField(County, blank=True, null=True)

    member_organization = models.ForeignKey(MemOrg, editable=False, blank=True)
    
    def __unicode__(self):
        return unicode(self.date) + self.title

    def happened(self):
        now = datetime.date.today()
        return now >= self.date

    def upcomming(self):
        now = datetime.date.today()
        return now <= self.date

    def data_entered(self):
        if self.postglean_set.count() != 0:
            return True
        return False

    @property
    def primary_location(self):
        if self.address_one:
            return self
        if (self.farm_location and hasattr(
                self.farm_location, 'instructions') and
                self.farm_location.instructions):
            return self.farm_location
        if (self.farm and hasattr(self.farm, 'instructions') and
                self.farm.instructions):
            return unicode(self.farm.instructions)

    def _address_one(self):
        return self.primary_location.address_one

    def _address_two(self):
        return self.primary_location.address_two

    def _city(self):
        return self.primary_location.city

    def _state(self):
        return self.primary_location.state

    def _zipcode(self):
        return self.primary_location.zipcode
        
    def render_instructions(self):
        if self.instructions:
            return unicode(self.instructions)
        if self.farm_location and hasattr(self.farm_location, 'instructions') and self.farm_location.instructions:
            return unicode(self.farm_location.instructions)
        if self.farm and hasattr(self.farm, 'instructions') and self.farm.instructions:
            return unicode(self.farm.instructions)
        else:
            return u"Show up early and have fun!"

    def render_address(self):
        if self.address_one:
            return unicode(self.address_one)
        if self.farm_location and hasattr(self.farm_location, 'instructions') and self.farm_location.instructions:
            return unicode(self.farm_location.instructions)
        if self.farm and hasattr(self.farm, 'instructions') and self.farm.instructions:
            return unicode(self.farm.instructions)
        else:
            return u"Show up early and have fun!"

    class Meta:
        permissions = (
            ("auth", "Member Organization Level Permissions"),
            ("uniauth", "Universal Permission Level"),
        )

class GleanForm(ModelForm):

    class Meta:
        model = GleanEvent
        exclude = ['invited_volunteers', 'attending_volunteers', 'officiated_by']
        widgets = {
            'date': TextInput({'class':'datepicker'}),
        }

class PostGlean(models.Model):
    glean = models.ForeignKey(GleanEvent, editable=False)
    user = models.ForeignKey(User, editable=False, null=True)
    attended = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    hours = models.IntegerField(default=0, null=True)
    hours = models.DecimalField("Hours (e.g. '3.5')", max_digits=5, decimal_places=3, blank=True, null=True)
    group = models.CharField(max_length=40, blank=True, null=True)
    members = models.CharField(max_length=20, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        returnable = unicode(self.glean.date)
        if hasattr(self, 'user') and self.user:
            returnable += ' - ' + unicode(self.user.username) 
        if hasattr(self, 'group') and self.group:
            returnable += ' - ' + unicode(self.group)
        if self.first_name and self.last_name and not self.user and not self.group:
            returnable += ' - ' + self.first_name + ' ' + self.last_name
        if not self.user and not self.group:
            returnable += ' - (unregistered)'

        return returnable

    class Meta:
        permissions = (
            ("auth", "Member Organization Level Permissions"),
            ("uniauth", "Universal Permission Level"),
        )

class PostGleanForm(ModelForm):
    class Meta:
        model = PostGlean
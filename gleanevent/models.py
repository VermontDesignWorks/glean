import datetime
from django.utils import timezone

from django.db import models
from django.forms import ModelForm
from django.forms.fields import ChoiceField


from django.conf import settings
from constants import VERMONT_COUNTIES

from django.contrib.auth.models import User
from farms.models import Farm, FarmLocation
from counties.models import County



# Create your models here.


class GleanEvent(models.Model):
	title = models.CharField(max_length=200)
	address_one = models.CharField("Address (line one)", max_length=200, blank=True)
	address_two = models.CharField("Address (line one)", max_length=200, blank=True)
	city = models.CharField("City", max_length=25, blank=True)
	state = models.CharField("State (Two Letter Abbreviation)", max_length=2, blank=True)

	date = models.DateTimeField('Date and Time', blank=True, null=True)
	description = models.TextField(blank=True)
	crops = models.CharField(max_length=200, blank=True)

	directions = models.TextField(blank=True, null=True)
	volunteers_needed = models.IntegerField(blank = True, default=0)
	duration = models.IntegerField(blank=True, default=1)

	farm = models.ForeignKey(Farm, blank=True, null=True)
	farm_location = models.ForeignKey(FarmLocation, blank=True, null=True)

	created_by = models.ManyToManyField(User, editable=False,  related_name="created_by")
	invited_volunteers = models.ManyToManyField(User, null=True, blank=True, related_name="invited_volunteers")
	rsvped = models.ManyToManyField(User, null=True, blank=True, related_name ="rsvped")
	not_rsvped = models.ManyToManyField(User, null=True, blank=True, related_name ="not_rsvped")
	attending_volunteers = models.ManyToManyField(User, null=True, blank=True, related_name="attending_voluntters")
	officiated_by = models.ManyToManyField(User, blank=True, related_name="officiated_by")
	counties = models.ManyToManyField(County, blank=True, null=True)

	#member_organization = models.ForeignKey('MemberOrganization')
	
	def __unicode__(self):
		return unicode(self.date) + self.title

	def upcomming_event(self):
		now = timezone.now()
		return now < self.date

class GleanForm(ModelForm):
	class Meta:
		model = GleanEvent
		exclude = ['invited_volunteers', 'attending_volunteers', 'officiated_by']

class PostGlean(models.Model):
	glean=models.ManyToManyField(GleanEvent, editable=False)
	person = models.ManyToManyField(User, editable=False)
	attended = models.BooleanField(default=False)
	first_name = models.CharField(max_length=20, blank=True, null=True)
	last_name = models.CharField(max_length=20, blank=True, null=True)
	hours = models.IntegerField(default=0)
	group = models.CharField(max_length=40, blank=True, null=True)
	members = models.CharField(max_length=20, blank=True, null=True)
	notes = models.CharField(max_length=200, blank=True, null=True)

class PostGleanForm(ModelForm):
	class Meta:
		model = PostGlean
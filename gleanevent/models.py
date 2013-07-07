import datetime

from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings
from django.forms.fields import ChoiceField

from constants import VERMONT_COUNTIES

from farms.models import Farm, FarmLocation
from counties.models import County


# Create your models here.


class GleanEvent(models.Model):
	title = models.CharField(max_length=200)
	address_one = models.CharField(max_length=200)
	address_two = models.CharField(max_length=200, blank=True)

	town = models.CharField(max_length=25, blank=True)
	date = models.DateTimeField('Date and Time', blank=True, null=True)
	description = models.TextField(blank=True)
	crops = models.CharField(max_length=200, blank=True)

	directions = models.TextField(blank=True, null=True)
	instructions = models.TextField(blank=True, null=True)


	farm = models.ForeignKey(Farm, blank=True, null=True)
	farm_location = models.ForeignKey(FarmLocation, blank=True, null=True)

	created_by = models.ManyToManyField(User, editable=False,  related_name="created_by")
	invited_volunteers = models.ManyToManyField(User, null=True, blank=True, related_name="invited_volunteers")
	#rsvped = models.ManyToManyField(User, null=True, blank=True, related_name ="rsvped")
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

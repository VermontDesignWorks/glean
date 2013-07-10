from django.db import models
from django.contrib import admin

from django.utils import timezone
import datetime
from django.forms.fields import ChoiceField
from constants import VERMONT_COUNTIES, LINE_TYPE, PHONE_TYPE, PREFERRED_CONTACT, FARM_TYPE

from django.forms import ModelForm

from django.contrib.auth.models import User
from django.conf import settings

from counties.models import County


# Create your models here.
class Farm(models.Model):
	name = models.CharField(max_length=200)
	farm_type = models.CharField(choices=FARM_TYPE, max_length=20)
	description = models.TextField(blank=True)

	physical_address_one = models.CharField('Physical Address (line one)', max_length=200, blank=True)
	physical_address_two = models.CharField('Physical Address (line two)',max_length=200, blank=True)
	physical_city = models.CharField('Physical Address (City)', max_length=200, blank=True)
	physical_state = models.CharField('Physical Address (State, Two Letter Code)', max_length=2, blank=True)
	physical_is_mailing = models.BooleanField('Physical Address is Mailing Address', default=True)

	mailing_address_one = models.CharField('Mailing Address (line one)', max_length=200, blank=True)
	mailing_address_two = models.CharField('Mailing Address (line two)',max_length=200, blank=True)
	mailing_city = models.CharField('Mailing Address (City)', max_length=200, blank=True)
	mailing_state = models.CharField('Mailing Address (State, Two Letter Code)', max_length=2, blank=True)

	phone_1 = models.CharField('Primary phone', max_length=200, blank=True)
	phone_1_type = models.CharField('Primary Phone Type',choices=LINE_TYPE,max_length=10,blank=True)
	phone_2 = models.CharField('Secondary phone', max_length=200, blank=True)
	phone_2_type = models.CharField('Secondary Phone Type', choices=LINE_TYPE,max_length=10,blank=True)

	email = models.CharField("The Farm's Email", max_length=200, blank=True)
	direction = models.TextField("Directions", blank=True)
	instructions = models.TextField("Instructions", blank=True)
	farmers = models.ManyToManyField(User, blank=True, null=True, editable=False)
	counties = models.ManyToManyField(County, blank=True, null=True)



	def __unicode__(self):
		return self.name

class FarmForm(ModelForm):
	class Meta:
		model = Farm
		exclude = ['farmers']

class FarmLocation(models.Model):
	farm = models.ForeignKey(Farm, blank=True, editable=False, null=True)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	directions = models.TextField(blank=True)
	counties = models.ManyToManyField(County, blank=True, null=True)

	def __unicode__(self):
		return self.farm.name + ' - ' + self.name


class LocationForm(ModelForm):
	class Meta:
		model = FarmLocation

class Contact(models.Model):
	farm = models.ForeignKey(Farm, blank=True, editable=False, null=True)
	first_name = models.CharField("First Name", max_length=20, blank=True)
	last_name = models.CharField("Last Name", max_length=20, blank=True)
	relation = models.CharField("Relationship to Farm", max_length=20, blank=True)
	email = models.EmailField("Email", blank=True, null=True)
	phone = models.CharField("Primary Phone", max_length=20, blank=True)
	phone_type = models.CharField("Phone Type", choices=PHONE_TYPE, max_length=2, blank=True)
	glean_contact = models.BooleanField("Should this person be contacted about gleans?", default=False)
	preferred = models.CharField("How Does this person Prefer to be Contacted?",choices=PREFERRED_CONTACT, max_length=1, blank=True, default='1')

class ContactForm(ModelForm):
	class Meta:
		model = Contact

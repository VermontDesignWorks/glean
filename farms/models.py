from django.db import models
from django.contrib import admin

from django.utils import timezone
import datetime
from django.forms.fields import ChoiceField
from constants import VERMONT_COUNTIES

from django.forms import ModelForm

from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Farm(models.Model):
	name = models.CharField(max_length=200)

	description = models.TextField(blank=True)
	contact_person_first_name = models.CharField(max_length=200, blank=True)
	contact_person_last_name = models.CharField(max_length=200, blank=True)
	address_one = models.CharField(max_length=200, blank=True)
	address_two = models.CharField(max_length=200, blank=True)
	phone_1 = models.CharField(max_length=200, blank=True)
	phone_2 = models.CharField(max_length=200, blank=True)
	email = models.CharField(max_length=200, blank=True)
	direction = models.TextField(blank=True)
	instructions = models.TextField(blank=True)
	farmers = models.ManyToManyField(User, blank=True, null=True)


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

	def __unicode__(self):
		return self.name


class LocationForm(ModelForm):
	class Meta:
		model = FarmLocation
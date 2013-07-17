from django.db import models
from django.forms import ModelForm

from constants import STATES
# Create your models here.

class Site(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	address_one = models.CharField(max_length=20, blank=True, null=True)
	address_two = models.CharField(max_length=20, blank=True, null=True)
	city = models.CharField(max_length=20, blank=True, null=True)
	state = models.CharField(max_length=2, choices=STATES, blank=True, null=True)
	zipcode = models.CharField(max_length=10, blank=True, null=True)
	
	def __unicode__(self):
		return self.name

class SiteForm(ModelForm):
	class Meta:
		model = Site

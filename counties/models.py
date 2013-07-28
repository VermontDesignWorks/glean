from django.db import models
from django.forms import ModelForm

from constants import STATES
# Create your models here.

class County(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	towns = models.TextField(max_length=200, blank=True)
	state = models.CharField(choices=STATES, max_length=2, default='VT')
	
	class Meta:
		permissions = (
			("uniauth", "Universal Permission Level"),
			)
	
	def __unicode__(self):
		return self.name

class CountyForm(ModelForm):
	class Meta:
		model = County

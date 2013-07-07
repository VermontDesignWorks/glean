from django.db import models
from django.forms import ModelForm

# Create your models here.

class County(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	towns = models.TextField(max_length=200, blank=True)
	
	def __unicode__(self):
		return self.name

class CountyForm(ModelForm):
	class Meta:
		model = County

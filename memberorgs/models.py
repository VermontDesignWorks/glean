from django.db import models
from django.forms import ModelForm

from constants import STATES
# Create your models here.

class MemOrg(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	counties = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

class MemOrgForm(ModelForm):
	class Meta:
		model = MemOrg
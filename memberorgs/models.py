from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from constants import STATES
# Create your models here.

class MemOrg(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	counties = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	volunteers = models.ManyToManyField(User, editable=False, related_name="member_organizations")
	
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
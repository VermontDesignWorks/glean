from django.db import models
from django.forms import ModelForm

from constants import STATES

from memberorgs.models import MemOrg

# Create your models here.

class RecipientSite(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	address_one = models.CharField(max_length=20, blank=True, null=True)
	address_two = models.CharField(max_length=20, blank=True, null=True)
	city = models.CharField(max_length=20, blank=True, null=True)
	state = models.CharField(max_length=2, choices=STATES, blank=True, null=True)
	zipcode = models.CharField(max_length=10, blank=True, null=True)
	member_organization = models.ForeignKey(MemOrg, editable=False, related_name="Member Organization")
	
	def __unicode__(self):
		return self.name

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

class SiteForm(ModelForm):
	class Meta:
		model = RecipientSite

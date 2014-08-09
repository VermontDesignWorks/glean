from django.db import models
from django.forms import ModelForm

from constants import STATES

from memberorgs.models import MemOrg

# Create your models here.

class RecipientSite(models.Model):
	name = models.CharField("Name", max_length=200)
	website = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	address_one = models.CharField(max_length=20, blank=True, null=True)
	address_two = models.CharField(max_length=20, blank=True, null=True)
	city = models.CharField(max_length=20, blank=True, null=True)
	state = models.CharField(max_length=2, choices=STATES, blank=True, null=True)
	zipcode = models.CharField(max_length=10, blank=True, null=True)
	member_organization = models.ForeignKey(MemOrg, editable=False, related_name="Member Organization")

	physical_is_mailing = models.BooleanField('Physical Address is Mailing Address', default=False)
	mailing_address_one = models.CharField('Mailing Address (line one)', max_length=200, blank=True)
	mailing_address_two = models.CharField('Mailing Address (line two)',max_length=200, blank=True)
	mailing_city = models.CharField('Mailing Address (City)', max_length=200, blank=True)
	mailing_state = models.CharField('Mailing Address (State)',choices=STATES, max_length=2, blank=True)
	mailing_zip = models.CharField('Mailing Address Zipcode', max_length=11, blank=True)

	primary_contact = models.CharField('Primary Contact First Name', max_length=30, blank=True)
	primary_contact = models.CharField('Primary Contact Last Name', max_length=30, blank=True)
	phone = models.CharField('Primary Phone', max_length=20, blank=True)
	email = models.CharField('Email', max_length=40, blank=True)

	
	def __unicode__(self):
		return self.name

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)
		ordering = ["name"]

class SiteForm(ModelForm):
	class Meta:
		model = RecipientSite

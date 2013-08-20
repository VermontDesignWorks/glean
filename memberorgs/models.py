from django.db import models

from counties.models import County

from django import forms
from django.contrib.auth.models import User

from django.contrib import admin
from constants import STATES, LINE_TYPE
# Create your models here.

class MemOrg(models.Model):
	name = models.CharField(max_length=200)
	website = models.CharField('Website', max_length=50, blank=True, null=True)
	description = models.TextField('Description', blank=True, null=True)
	counties = models.ManyToManyField(County, blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	volunteers = models.ManyToManyField(User, editable=False, related_name="member_organizations")

	address_one = models.CharField('Physical Address (line one)', max_length=30, blank=True, null=True)
	address_two = models.CharField('Physical Address (line two)', max_length=30, blank=True, null=True)
	city = models.CharField('City', max_length=15, blank=True, null=True)
	state = models.CharField("State",choices=STATES, default="VT", max_length=2, blank=True)
	zipcode = models.CharField("Zipcode", max_length=11, blank=True, null=True)
	physical_is_mailing = models.BooleanField('Physical Address is Mailing Address', default=True)

	mailing_address_one = models.CharField('Mailing Address (line one)', max_length=200, blank=True)
	mailing_address_two = models.CharField('Mailing Address (line two)',max_length=200, blank=True)
	mailing_city = models.CharField('Mailing Address (City)', max_length=200, blank=True)
	mailing_state = models.CharField('Mailing Address (State)',choices=STATES, max_length=2, blank=True)
	mailing_zip = models.CharField('Mailing Address Zipcode', max_length=11, blank=True)

	phone_1 = models.CharField('Primary phone', max_length=200, blank=True)
	phone_1_type = models.CharField('Primary Phone Type',choices=LINE_TYPE,max_length=10,blank=True)
	phone_2 = models.CharField('Secondary phone', max_length=200, blank=True)
	phone_2_type = models.CharField('Secondary Phone Type', choices=LINE_TYPE,max_length=10,blank=True)

	first_name = models.CharField("Executive Director First Name", max_length=20)
	last_name = models.CharField("Executive Director Last Name", max_length=20)
	phone = models.CharField("Director's Direct Phone Number", max_length=15, blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

class MemOrgForm(forms.ModelForm):
	class Meta:
		model = MemOrg

class MemOrgCombinedForm(MemOrgForm):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)
	verify = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=20)
	last_name = forms.CharField(max_length=20)
	phone = forms.CharField(max_length=20)
	def is_valid(self):
		if password != verify:
			return False
		return super(MemOrgCombinedForm, self).is_valid()

	def save(self, *args, **kwargs):
		user = User.objects.create_user(username=username, password=password, email=email)
		profile = Profile(user=user, first_name=first_name, last_name=last_name, phone=phone)
		super(MemOrgCombinedForm, self).save(*args, **kwargs)
		

admin.site.register(MemOrg)
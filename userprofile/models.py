from django.db import models
from django.contrib.auth.models import User
from django import forms
#from registration.forms import RegistrationForm
#from registration.backends.default import DefaultBackend

from constants import ACCESS_LEVELS, VERMONT_COUNTIES, AGE_RANGES
from django.conf import settings
from counties.models import County


def_max_length = 255

class Profile(models.Model):
	user = models.ForeignKey(User, blank=True, unique=True, editable=False)
	access = models.CharField(max_length=20, choices=ACCESS_LEVELS, default="VO", editable=False)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	address = models.CharField(max_length=200, blank=True)
	city = models.CharField(max_length=200, blank=True)
	counties = models.ManyToManyField(County, blank=True, null=True)
	age = models.CharField(max_length=200,
							choices=AGE_RANGES,
							blank=True)
	phone = models.CharField(max_length=200, blank=True)
	ecfirst_name = models.CharField(max_length=200, blank=True)
	eclast_name = models.CharField(max_length=200, blank=True)
	ecphone = models.CharField(max_length=200, blank=True)
	ecrelationship = models.CharField(max_length=200, blank=True)
	accepts_email = models.BooleanField(default=True, editable=False)
	mo_emails_only = models.BooleanField(default=False)
	member_organization = models.CharField(max_length=200, blank=True)


		
	def __unicode__(self):
		return u'%s %s' % (self.user, self.address)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile

class UserForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)
	verify = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)
	email = forms.EmailField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)

class EmailForm(forms.Form):
	email = forms.EmailField()





try:
	admin.site.register(Profile)
except:
	pass

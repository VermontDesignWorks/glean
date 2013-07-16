from django.db import models
from django.contrib.auth.models import User
from django import forms
#from registration.forms import RegistrationForm
#from registration.backends.default import DefaultBackend

from constants import ACCESS_LEVELS, VERMONT_COUNTIES, AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, STATES
from django.conf import settings
from counties.models import County

class Profile(models.Model):
	user = models.ForeignKey(User, blank=True, unique=True, editable=False)
	#access = models.CharField(max_length=20, choices=ACCESS_LEVELS, default="VO", editable=False)

	first_name = models.CharField("First Name", max_length=20)
	last_name = models.CharField("Last Name", max_length=20)
	address = models.CharField("Address (line one)", max_length=200, blank=True)
	city = models.CharField("City", max_length=200, blank=True)
	state = models.CharField("State", max_length=2, choices=STATES)
	counties = models.ManyToManyField(County, blank=True, null=True, related_name='people')
	age = models.CharField("Age", max_length=200,
							choices=AGE_RANGES,
							blank=True)
	phone = models.CharField("Primary Phone", max_length=200, blank=True)
	phone_type = models.CharField("Phone Type", choices=PHONE_TYPE, max_length=1, default='1')
	mo_emails_only = models.BooleanField(default=False)
	preferred_method = models.CharField(choices=PREFERRED_CONTACT, max_length=1, default='1')
	#member_organization = models.ForeignKey(member_organization)

	ecfirst_name = models.CharField("Emergency Contact First Name", max_length=200, blank=True)
	eclast_name = models.CharField("Emergency Contact Last Name", max_length=200, blank=True)
	ecphone = models.CharField("Emergency Contact Phone", max_length=200, blank=True)
	ecrelationship = models.CharField("Relationship", max_length=200, blank=True)
	
	accepts_email = models.BooleanField(default=True, editable=False)
	unsubscribe_key = models.CharField("Unsubscribe key, for emails", max_length=30, blank=True, null=True, editable=False)
			
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

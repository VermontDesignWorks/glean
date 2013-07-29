from registration.forms import RegistrationForm
from django import forms
from constants import ACCESS_LEVELS, VERMONT_COUNTIES, AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, STATES

class ExtendedRegistrationForm(RegistrationForm):
	

	first_name = forms.CharField(label="First Name", max_length=20)
	last_name = forms.CharField(label="Last Name", max_length=20)
	address = forms.CharField(label="Address (line one)", max_length=200, blank=True)
	city = forms.CharField(label="City", max_length=200, blank=True)
	state = forms.ChoiceField(label="State", max_length=2, choices=STATES, default='VT')
	counties = forms.ModelChoiceField(queryset=County.objects.all(), blank=True)
	age = forms.ChoiceField(label="Age", max_length=2,
							choices=AGE_RANGES,
							blank=True)
	phone = forms.CharField(label="Primary Phone", max_length=200, blank=True)
	phone_type = forms.ChoiceField(label="Phone Type", choices=PHONE_TYPE, max_length=1, default='1')
	preferred_method = forms.ChoiceField(label="How Should We Contact You?",choices=PREFERRED_CONTACT, max_length=1, default='1')
	member_organization = forms.ModelChoiceField(MemOrg)

	ecfirst_name = forms.CharField(label="Emergency Contact First Name", max_length=200, blank=True)
	eclast_name = forms.CharField(label="Emergency Contact Last Name", max_length=200, blank=True)
	ecphone = forms.CharField(label="Emergency Contact Phone", max_length=200, blank=True)
	ecrelationship = forms.CharField(label="Relationship", max_length=200, blank=True)
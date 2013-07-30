from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm

from django.http import HttpResponse

from counties.models import County
from memberorgs.models import MemOrg
from userprofile.models import Profile

from django import forms
from constants import ACCESS_LEVELS, VERMONT_COUNTIES, AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, STATES

class ExtendedRegistrationForm(RegistrationForm):
	first_name = forms.CharField(label="First Name", max_length=20)
	last_name = forms.CharField(label="Last Name", max_length=20)
	address = forms.CharField(label="Address (line one)", max_length=200)
	city = forms.CharField(label="City", max_length=200)
	state = forms.ChoiceField(label="State",choices=STATES, initial='VT')
	counties = forms.ModelMultipleChoiceField(queryset=County.objects.all())
	age = forms.ChoiceField(label="Age",
							choices=AGE_RANGES)
	phone = forms.CharField(label="Primary Phone", max_length=200)
	phone_type = forms.ChoiceField(label="Phone Type", choices=PHONE_TYPE,initial='1')
	preferred_method = forms.ChoiceField(label="How Should We Contact You?",choices=PREFERRED_CONTACT,initial='1')
	member_organization = forms.ModelChoiceField(queryset=MemOrg.objects.all())

	ecfirst_name = forms.CharField(label="Emergency Contact First Name", max_length=200)
	eclast_name = forms.CharField(label="Emergency Contact Last Name", max_length=200)
	ecphone = forms.CharField(label="Emergency Contact Phone", max_length=200)
	ecrelationship = forms.CharField(label="Relationship", max_length=200)


class MyRegistrationView(RegistrationView):
	form_class = ExtendedRegistrationForm
	#def get_form(self,request):
	#		return ExtendedRegistrationForm

	def register(self, *args, **kwargs):
		form = self.get_form(ExtendedRegistrationForm)
		form.is_valid()
		user = super(MyRegistrationView, self).register(*args, **kwargs)
		
		profile = Profile(first_name=form.cleaned_data['first_name'],
			last_name=form.cleaned_data['last_name'],
			address=form.cleaned_data['address'],
			city=form.cleaned_data['city'],
			state=form.cleaned_data['state'],
			age=form.cleaned_data['age'],
			phone=form.cleaned_data['phone'],
			phone_type=form.cleaned_data['phone_type'],
			preferred_method=form.cleaned_data['preferred_method'],
			ecfirst_name=form.cleaned_data['ecfirst_name'],
			eclast_name=form.cleaned_data['eclast_name'],
			ecrelationship=form.cleaned_data['ecrelationship'],
			user=user,
			member_organization=form.cleaned_data['member_organization'],
			)
		profile.save()
		for county in form.cleaned_data['counties']:
			profile.counties.add(county)
		return user


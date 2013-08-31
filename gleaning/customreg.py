from registration.backends.default.views import RegistrationView, ActivationView
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
	address_one = forms.CharField(label="Address", max_length=200)
	address_two = forms.CharField(label="Address (line two)", max_length=200, required=False)
	city = forms.CharField(label="City", max_length=200)
	state = forms.ChoiceField(label="State",choices=STATES, initial='VT')
	zipcode = forms.CharField(label="Zipcode", max_length=11, required=False)
	counties = forms.ModelMultipleChoiceField(queryset=County.objects.all(), label="Counties You'd like to Glean In")
	age = forms.ChoiceField(label="Age",
							choices=AGE_RANGES)
	phone = forms.CharField(label="Primary Phone", max_length=200)
	phone_type = forms.ChoiceField(label="Phone Type", choices=PHONE_TYPE,initial='1')
	preferred_method = forms.ChoiceField(label="How Should We Contact You?",choices=PREFERRED_CONTACT,initial='1')
	#member_organization = forms.ModelChoiceField(queryset=MemOrg.objects.all())

	ecfirst_name = forms.CharField(label="Emergency Contact First Name", max_length=200)
	eclast_name = forms.CharField(label="Emergency Contact Last Name", max_length=200)
	ecphone = forms.CharField(label="Emergency Contact Phone", max_length=200)
	ecrelationship = forms.CharField(label="Relationship", max_length=200)

	waiver = forms.BooleanField(label="Do you accept the Waiver of Liability?", required=True)

	agreement = forms.BooleanField(label="Do you accept the Volunteer Agreement?", required=True)
	# seriously?
	photo_release = forms.BooleanField(label="Do you accept the Photo Release?")

	opt_in = forms.BooleanField(label="Do you wish to recieve newsletters and personalized messages?")

class AdminExtendedRegistrationForm(RegistrationForm):
	first_name = forms.CharField(label="First Name", max_length=20)
	last_name = forms.CharField(label="Last Name", max_length=20)
	address_one = forms.CharField(label="Address", max_length=200, required=False)
	address_two = forms.CharField(label="Address (line two)", max_length=200, required=False)
	city = forms.CharField(label="City", max_length=200, required=False)
	state = forms.ChoiceField(label="State",choices=STATES, initial='VT', required=False)
	zipcode = forms.CharField(label="Zipcode", max_length=11, required=False)
	counties = forms.ModelMultipleChoiceField(queryset=County.objects.all(), label="Counties", required=False)
	age = forms.ChoiceField(label="Age",
							choices=AGE_RANGES, required=False)
	phone = forms.CharField(label="Primary Phone", max_length=200, required=False)
	phone_type = forms.ChoiceField(label="Phone Type", choices=PHONE_TYPE,initial='1', required=False)
	preferred_method = forms.ChoiceField(label="Primary Contact Method",choices=PREFERRED_CONTACT,initial='1', required=False)
	#member_organization = forms.ModelChoiceField(queryset=MemOrg.objects.all())

	ecfirst_name = forms.CharField(label="Emergency Contact First Name", max_length=200, required=False)
	eclast_name = forms.CharField(label="Emergency Contact Last Name", max_length=200, required=False)
	ecphone = forms.CharField(label="Emergency Contact Phone", max_length=200, required=False)
	ecrelationship = forms.CharField(label="Relationship", max_length=200, required=False)

	waiver = forms.BooleanField(label="Waiver of Liability?", required=True)
	agreement = forms.BooleanField(label="Volunteer Agreement", required=True)
	# seriously?
	photo_release = forms.BooleanField(label="Photo Release?", required=False)
	opt_in = forms.BooleanField(label="Email Opt-In?", required=False)


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
			address_one=form.cleaned_data['address_one'],
			address_two=form.cleaned_data['address_two'],
			city=form.cleaned_data['city'],
			state=form.cleaned_data['state'],
			zipcode=form.cleaned_data['zipcode'],
			age=form.cleaned_data['age'],
			phone=form.cleaned_data['phone'],
			phone_type=form.cleaned_data['phone_type'],
			ecphone = form.cleaned_data['ecphone'],
			preferred_method=form.cleaned_data['preferred_method'],
			ecfirst_name=form.cleaned_data['ecfirst_name'],
			eclast_name=form.cleaned_data['eclast_name'],
			ecrelationship=form.cleaned_data['ecrelationship'],
			user=user,
			waiver = form.cleaned_data['waiver'],
			agreement = form.cleaned_data['agreement'],
			photo_release = form.cleaned_data['photo_release'],
			opt_in = form.cleaned_data['opt_in']
			)
		profile.save()
		for county in form.cleaned_data['counties']:
			profile.counties.add(county)
			county.affix_to_memorgs(user)
		return user

# class MyActivationView(ActivationView):
# 	def activate(self, *args, **kwargs):
# 		user = super(MyActivationView, self).activate(*args, **kwargs)
# 		profile = user.profile_set.get()
# 		counties = profile.counties.all()
# 		memorgs = []
# 		for county in counties:
# 			for memorg in couny.member_organization_set.all():
# 				quick_mail(subject, text, recipient)
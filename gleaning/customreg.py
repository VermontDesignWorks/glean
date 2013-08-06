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
	address = forms.CharField(label="Address", max_length=200)
	city = forms.CharField(label="City", max_length=200)
	state = forms.ChoiceField(label="State",choices=STATES, initial='VT')
	counties = forms.ModelMultipleChoiceField(queryset=County.objects.all())
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

	waiver = forms.BooleanField(label="Waiver of Liability", required=True)
	# I understand that Salvation Farms is designed to let me harvest and process surplus farm produce for donation 
	# to vulnerable populations in Vermont through connection with local and state agencies that serve the food 
	# and nutritionally insecure.  I understand that I must work safely and treat participating farm and kitchen 
	# properties with respect and care.
	# With this knowledge, I _______________________________, and anyone accompanying me, do hereby 
	# expressly agree that all our activities shall be at our sole risk and that neither Salvation Farms volunteers or its
	# project leaders, nor the donors whose property we enter shall be held liable for any claims, demands, injuries, 
	# damages, actions, or causes of action whatsoever, to person or property arising out of or connected with our 
	# participation in this farm surplus management project.
	agreement = forms.BooleanField(label="Volunteer Agreement", required=True)
	# seriously?
	photo_release = forms.BooleanField(label="Photo Release")
	# I, ____________________, hereby authorize Salvation Farms permission to use my likeness in a photograph in 
	# any and all of its publications, including but not limited to all Salvation Farms printed and digital publications.  
	# I understand and agree that any photograph using my likeness will become property of Salvation Farms and 
	# will not be returned.
	# I acknowledge that since my participation with Salvation Farms is voluntary, I will receive no financial 
	# compensation.
	# I hereby irrevocably authorize Salvation Farms to edit, alter, copy, exhibit, publish or distribute photos for 
	# purposes of publicizing Salvation Farms programs or for any other lawful purpose.  In addition, I waive the 
	# tight to inspect or approve the finished product, including written or electronic copy, wherein my likeness 
	# appears.  Additionally, I waive any tight to royalties or other compensation arising or related to the use of 
	# photographs.
	# I hereby hold harmless and release and forever discharge Salvation Farms from all claims, demands, and 
	# causes of action which I, my heirs, representative, executors, administrators, or any other person acting on my 
	# behalf or on behalf of my estate have or may have by reason of this authorization.
	# I am at least 18 years of age and am competent to contract in my own name. I have read this release before 
	# signing below and I fully understand the contents, meaning and impact of this release.


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
			#member_organization=form.cleaned_data['member_organization'],
			)
		profile.save()
		for county in form.cleaned_data['counties']:
			profile.counties.add(county)
		return user


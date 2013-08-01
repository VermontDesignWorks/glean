# Create your views here.
import csv

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm, EmailForm, EditProfileForm
from constants import VERMONT_COUNTIES

from django import forms
from gleaning.customreg import ExtendedRegistrationForm

@login_required
def userDetailEntry(request):
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			if not Profile.objects.filter(user=request.user).exists():
				new_save = form.save(commit=False)
				new_save.user = request.user
				new_save.save()
			else:
				form = ProfileForm(request.POST, Profile.objects.filter(user=request.user).get())
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':"form wasn't valid"})
	else:
		form = ProfileForm
		return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':''})

@login_required
def selfEdit(request):
	if request.method == "POST":
		instance = Profile.objects.get(user=request.user)
		form = EditProfileForm(request.POST, instance=instance)
		if form.is_valid():
			new_save = form.save(commit=False)
			#new_save.member_organization = instance.member_organization
			new_save.save()
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':"form wasn't valid (try filling in more stuff)",'editmode':True})
	else:
		if Profile.objects.filter(user=request.user).exists():
			profile = Profile.objects.get(user=request.user)
			form = EditProfileForm(instance = profile)
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':'','editmode':True})
		else:
			form = EditProfileForm()
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':'','editmode':True})

@permission_required('userprofile.auth')
def userLists(request):
	if request.user.has_perm('userprofile.uniauth'):
		users = Profile.objects.all()
	else:
		users = Profile.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	return render(request, 'userprofile/userLists.html', {'users':users})

@permission_required('userprofile.auth')
def userProfile(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	if user.profile_set.get().member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('userprofile.uniauth'):
		return HttpResponseRedirect('home')
	person = Profile.objects.get(user=user)
	return render(request, 'userprofile/detail.html', {'person':person})

@permission_required('userprofile.auth')
def userEdit(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	if user.profile_set.get().member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('userprofile.uniauth'):
		return HttpResponseRedirect('home')
	person = Profile.objects.get(user=user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, person)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.user = user
			new_save.id = person.id
			new_save.save()
			return HttpResponseRedirect(reverse('userprofile:userlists'))
		else:
			
			return render(request, 'userprofile/adminedit.html', {'person':person, 'profile':person, 'form':form})			

	else:
		form = ProfileForm(instance=person)
		return render(request, 'userprofile/adminedit.html', {'person':person, 'profile':person, 'form':form})

def emailEdit(request):
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			request.user.email = form.cleaned_data['email']
			request.user.save()
			return HttpResponseRedirect(reverse('home'))
		else:
			form = EmailForm()
			return render(request, 'userprofile/emailedit.html', {'error':"That's not a valid address", 'form':form})
	else:
		form = EmailForm()
		return render(request, 'userprofile/emailedit.html',{'form':form})

@permission_required('userprofile.auth')
def download(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=user_profiles.csv'

	# Create the CSV writer using the HttpResponse as the "file."
	writer = csv.writer(response)
	writer.writerow([
	'Username',
	'Access',
	'First Name',
	'Last Name',
	'Address',
	'City',
	'State',
	'Counties',
	'Age Bracket',
	'Phone',
	'Phone Type',
	'Primary Member Org',
	'Primary MO Only',
	'Contact Method',
	"Seconary MO's",
	'EC First',
	'EC Last',
	'EC Phone',
	'EC Relationship',
	'Accepts Email',
	])

	if request.user.has_perm('userprofile.uniauth'):
		profiles = Profile.objects.all()
	else:
		profiles = Profile.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	for profile in profiles:
		writer.writerow([
			profile.user.username,
			profile.user.groups.all(),
			profile.last_name,
			profile.first_name,
			profile.address,
			profile.city,
			profile.state,
			profile.counties.all(),
			profile.age,
			profile.phone,
			profile.phone_type,
			profile.member_organization,
			profile.mo_emails_only,
			profile.preferred_method,
			profile.secondary_member_organizations.all(),
			profile.ecfirst_name,
			profile.eclast_name,
			profile.ecphone,
			profile.ecrelationship,
			profile.accepts_email,
			])

	return response

@permission_required('userprofile.auth')
def newUser(request):
	if request.method == 'POST':
		form = ExtendedRegistrationForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
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
			user=new_user,
			member_organization=request.user.profile_set.get().member_organization,
			)
			profile.save()
			return HttpResponseRedirect(reverse('userprofile:userlists'))
	else:
		form = ExtendedRegistrationForm()
	return render(request, 'userprofile/newuser.html', {'form':form})
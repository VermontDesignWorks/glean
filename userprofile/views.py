# Create your views here.
import csv

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm, EmailForm, EditProfileForm, UniPromoteForm, PromoteForm
from memberorgs.models import MemOrg
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
		users = Profile.objects.all().order_by('member_organization', 'last_name')
	else:
		users = Profile.objects.filter(member_organization=request.user.profile_set.get().member_organization).order_by('last_name')
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
			new_save.member_organization = person.member_organization
			new_save.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse('userprofile:userprofile', args=(user_id,)))
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
	'Member Org',
	'Primary MO Only',
	'Contact Method',
	"Join Date",
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
			profile.joined,
			profile.ecfirst_name,
			profile.eclast_name,
			profile.ecphone,
			profile.ecrelationship,
			profile.accepts_email,
			])

	return response

@permission_required('userprofile.auth')
def newUser(request):
	notice = ''
	if request.method == 'POST':
		form = ExtendedRegistrationForm(request.POST)
		if form.is_valid():
			new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
			profile = Profile(
				first_name=form.cleaned_data['first_name'],
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
			notice = 'New Volunteer ' + profile.first_name + ' ' + profile.last_name + ' has been created.'
			#return HttpResponseRedirect(reverse('userprofile:userlists'))
	else:
		form = ExtendedRegistrationForm()
	if request.user.has_perm('userprofile.uniauth'):
		users = Profile.objects.all().order_by('-joined')[:20]
	else:
		users = Profile.objects.filter(member_organization=request.user.profile_set.get().member_organization).order_by('-joined')[:20]
	return render(request, 'userprofile/newuser.html', {'form':form, 'users':users, 'notice':notice})

@permission_required('userprofile.auth')
def userPromote(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	profile=user.profile_set.get()
	ed = Group.objects.get(name="Member Organization Executive Director")
	memc = Group.objects.get(name="Member Organization Glean Coordinator")
	sal = Group.objects.get(name="Salvation Farms Administrator")
	salc = Group.objects.get(name="Salvation Farms Coordinator")

	executive = ed in user.groups.all() or sal in user.groups.all()
	admin = executive or memc in user.groups.all() or salc in user.groups.all()
	data = {'member_organization':profile.member_organization,
			'executive': executive,
			'promote':admin}
	member_organization = forms.ModelChoiceField(queryset=MemOrg.objects.all(), label="Member Organization", empty_label=None)

	## GIANT Promotion cluster. Salvation Farms can do real and meaningful changes to person data
	## And member organizations can promote/demote coordinators for their Member Organization, no more, no less.
	if request.user.has_perm('userprofile.uniauth'):#is this a sal farms person?
		if request.method == 'POST': #if you're getting data
			form = UniPromoteForm(request.POST) #save it
			if form.is_valid(): #validate it
				user.groups.clear() #if it's valid, clear your groups data
				profile.member_organization = form.cleaned_data['member_organization'] # save your member org data
				profile.save()
				if form.cleaned_data['promote']: #in the case this is a PROmotion
					# this next step asks if, as only salvation farm users, or 'sal' users,
					# can access this form, if we're
					# adding another to the fold
					if form.cleaned_data['member_organization'] == request.user.profile_set.get().member_organization:
						if form.cleaned_data['executive']: #executive if/else
							user.groups.add(sal)
						else: 
							user.groups.add(salc)
					else: # not making a sal users->
						if executive: #executive if/else
							user.groups.add(ed)
						else:
							user.groups.add(memc)
					return HttpResponseRedirect(reverse('userprofile:userprofile', args=(user_id,)))
				else:
					# in the case this is a DEmotion, we've already
					# cleared user.groups and retained memorg distinction
					# if it was there, so redirect to the userprofile page
					return HttpResponseRedirect(reverse('userprofile:userprofile', args=(user_id,)))
			else:
				return render(request, 'userprofile/user_promote.html', {'form':form})
		else:
			form = UniPromoteForm(data) #not a POST, so fill in the data

	else: #this is apparently not a sal farms person
		if request.method == 'POST':
			form = PromoteForm(request.POST)
			if form.is_valid():
				if executive == False: #if we're not messing with the boss's status
					user.groups.clear()
					if form.cleaned_data['promote']:
						user.groups.add(memc)
				else:
					return HttpResponseRedirect(reverse('userprofile:userprofile', args=(user.id,)))
			return HttpResponseRedirect(reverse('userprofile:userprofile', args=(user_id,)))
		else:
			form = PromoteForm({'promote':admin}) #not a POST, so fill in the 'promote' field
	return render(request, 'userprofile/user_promote.html', {'form':form})
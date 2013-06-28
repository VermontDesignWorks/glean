# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm
from constants import VERMONT_COUNTIES

def userReg(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('userprofile:userhome'))
	if request.method =="POST":
		form = UserForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['password'] == form.cleaned_data['verify']:
				if not User.objects.filter(username=form.cleaned_data['username']):
					newUser = User.objects.create_user(form.cleaned_data['username'],
													form.cleaned_data['email'],
													form.cleaned_data['password'])
					user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
					login(request, user)
					return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
				else:
					error = "that username is already Taken"
			else:
				error = "your passwords didn't match"
		return render(request, 'userprofile/registration.html', {'form':form, 'error':error})
	form = UserForm()
	return render(request, 'userprofile/registration.html', {'form':form, 'user':'request.method != post'})

@login_required
def userDetailEntry(request):
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			try:
				profile = Profile.objects.get(user=request.user)
			except:
				profile = Profile(**form.cleaned_data)
				profile.user = request.user
				profile.save()
			#return HttpResponse(str(profile.user))
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':"form wasn't valid"})
	else:
		form = ProfileForm
		return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':''})

@login_required
def selfEdit(request):
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			try:
				old_prof = Profile.objects.get(user=request.user)
				new_prof = Profile(**form.cleaned_data)
				new_prof.id = old_prof.id
				new_prof.user = request.user
				new_prof.save()
				return HttpResponseRedirect(reverse('home'))
			except:
				profile = Profile(**form.cleaned_data)
				profile.user = request.user
				profile.save()
				return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':"form wasn't valid (try filling in more stuff)"})
	else:
		try:
			profile = Profile.objects.get(user=request.user)
		except:
			return HttpResponseRedirect(reverse('userprofile:userdetailentry'))
		form = ProfileForm(instance = profile)
		#return HttpResponse('test')
		return render(request, 'userprofile/userEdit.html', {'form':form, 'error':''})

def userLists(request):
	users = Profile.objects.all()
	return render(request, 'userprofile/userLists.html', {'users':users, 'error':''})

@login_required
def userProfile(request, user_id):
	user_id_object = get_object_or_404(User, pk=user_id)
	person = Profile.objects.get(user=user_id_object)
	return render(request, 'userprofile/detail.html', {'person':person})

def userEdit(request, user_id):
	person = get_object_or_404(User, pk=user_id)
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			try:
				old_prof = Profile.objects.get(user=person)
				new_prof = Profile(**form.cleaned_data)
				new_prof.id = old_prof.id
				new_prof.user = person
				new_prof.save()
				return HttpResponseRedirect(reverse('userprofile:userlists'))
			except:
				profile = Profile(**form.cleaned_data)
				profile.user = person
				profile.save()
				return HttpResponseRedirect(reverse('userprofile:userlists'))

	else:
		person = get_object_or_404(User, pk=user_id)
		try:
			profile = Profile.objects.get(user=person)
			form = ProfileForm(instance = profile)
		except:
			profile = ''
			form = ProfileForm()
		return render(request, 'userprofile/adminedit.html', {'person':person, 'profile':profile, 'form':form})
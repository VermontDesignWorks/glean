# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm

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
			profile = Profile(**form.cleaned_data)
			profile.user = request.user
			profile.save()
			return HttpResponseRedirect(reverse('userprofile:userhome'))
		else:
			return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':"form wasn't valid"})
	else:
		form = ProfileForm
		return render(request, 'userprofile/userdetailentry.html', {'form':form, 'error':''})



def userLogin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('userprofile:userhome'))
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('userprofile:userhome'))
				else:
					return render(request, 'userprofile/login.html', {'form':form, 'error':'Account is Disabled'})					
			else:
				return render(request, 'userprofile/login.html', {'form':form, 'error':'Username or Password is incorrect'})					
		else:
			return render(request, 'userprofile/login.html', {'form':form, 'error':'Form was filled out incorrectly'})					
	else:
		form = LoginForm()
		return render(request, 'userprofile/login.html', {'form':form, 'error':''})					

def userLogout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def userHome(request):
	return render(request, 'userprofile/home.html')

@login_required
def userProfile(request):
	return HttpResponse('this has nothing so far')

@login_required
def editProfile(request):
	return HttpResponse('this has nothing so far')
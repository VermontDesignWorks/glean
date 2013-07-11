# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from userprofile.models import Profile, ProfileForm, UserForm, LoginForm, EmailForm
from constants import VERMONT_COUNTIES

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
		form = ProfileForm(request.POST, instance=Profile.objects.get(user=request.user))
		if form.is_valid():
			new_save = form.save()
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':"form wasn't valid (try filling in more stuff)",'editmode':True})
	else:
		if Profile.objects.filter(user=request.user).exists():
			profile = Profile.objects.get(user=request.user)
			form = ProfileForm(instance = profile)
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':'','editmode':True})
		else:
			form = ProfileForm()
			return render(request, 'userprofile/userEdit.html', {'form':form, 'error':'','editmode':True})


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
		return render(request, 'userprofile/adminedit.html', {'person':person, 'profile':profile, 'form':form, 'editmode':True})

def emailEdit(request):
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			request.user.email = form.cleaned_data['email']
			request.user.save()
			return HttpResponseRedirect(reverse('home'))
		else:
			form = EmailForm()
			return render(request, 'userprofile/emailedit.html', {'error':"That's not a valid address", 'form':form, 'editmode':True})
	else:
		form = EmailForm()
		return render(request, 'userprofile/emailedit.html',{'form':form})

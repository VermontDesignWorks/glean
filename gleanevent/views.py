import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required

from gleanevent.models import GleanEvent, GleanForm

def index(request):
	gleaning_events_list = GleanEvent.objects.all()
	return render(request, 'gleanevent/index.html', {'gleans':gleaning_events_list})

def newGlean(request):
	if request.method == "POST":
		form = GleanForm(request.POST)
		if form.is_valid():
			#newGlean = GleanEvent(**form.cleaned_data)
			#newGlean.save()
			new_save = form.save()
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(new_save.id,) ))
		return HttpResponse('form was not valid')
			
	else:
		form = GleanForm()
		return render(request, 'gleanevent/new.html', {'form':form})

def editGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if request.method == "POST":
		form = GleanForm(request.POST, instance = glean)
		if form.is_valid():
			#newGlean = GleanEvent(**form.cleaned_data)
			#newGlean.id = glean_id
			#newGlean.save()
			new_save = form.save()
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(new_save.id,) ))
	form = GleanForm(instance = glean)
	return render(request, 'gleanevent/edit.html', {'form':form, 'glean':glean , 'editmode':True})

@login_required
def detailGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	return render(request, 'gleanevent/detail.html', {'glean':glean})

def gleanCalendar(request):
	gleans = GleanEvent.objects.all()
	return render(request, 'gleanevent/calendar.html', {'gleans':gleans})

def announceGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	return render(request, 'gleanevent/announce.html', {'glean':glean})

def confirmLink(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if request.user not in glean.rsvped.all():
		glean.rsvped.add(request.user)
		if request.user in glean.not_rsvped.all():
			glean.not_rsvped.remove(request.user)
		glean.save()
	return render(request, 'gleanevent/confirm.html', {'glean':glean})

def denyLink(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if request.user not in glean.not_rsvped.all():
		glean.not_rsvped.add(request.user)
		if request.user in glean.rsvped.all():
			glean.rsvped.remove(request.user)
		glean.save()
	return render(request, 'gleanevent/deny.html', {'glean':glean})

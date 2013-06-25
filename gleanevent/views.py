import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms

from gleanevent.models import GleanEvent, GleanForm

def index(request):
	gleaning_events_list = GleanEvent.objects.all()
	return render(request, 'gleanevent/index.html', {'gleans':gleaning_events_list})

def newGlean(request):
	if request.method == "POST":
		form = GleanForm(request.POST)
		if form.is_valid():
			newGlean = GleanEvent(**form.cleaned_data)
			newGlean.save()
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(newGlean.id,) ))
		return HttpResponse('form was not valid')
			
	else:
		form = GleanForm()
		return render(request, 'gleanevent/new.html', {'form':form})

def editGlean(request, glean_id):
	if request.method == "POST":
		form = GleanForm(request.POST)
		if form.is_valid():
			newGlean = GleanEvent(**form.cleaned_data)
			newGlean.id = glean_id
			newGlean.save()
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(newGlean.id,) ))
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	form = GleanForm(instance = glean)
	return render(request, 'gleanevent/edit.html', {'form':form, 'glean':glean})

def detailGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	return render(request, 'gleanevent/detail.html', {'glean':glean})

def gleanCalendar(request):
	gleans = GleanEvent.objects.all()
	return render(request, 'gleanevent/calendar.html', {'gleans':gleans})
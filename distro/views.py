# Create your views here.
import time
import datetime
import csv

import django.forms
from django.forms.widgets import TextInput
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms

from django.contrib.auth.decorators import permission_required

from django.forms.models import modelformset_factory

from distro.models import Distro

@permission_required('distro.auth')
def entry(request):
	DistroFormSet = modelformset_factory(Distro, extra=int(50))
	if request.method == 'POST':
		formset = DistroFormSet(request.POST)
		formset.is_valid()
		#	pass
		#else:
	#		return HttpResponse(formset.errors)
		instances = formset.save(commit=False)
		for instance in instances:
			instance.member_organization = request.user.profile_set.get().member_organization
			instance.save()
		return HttpResponseRedirect(reverse('distro:entry'))
	else:
		form = DistroFormSet(queryset=Distro.objects.none())
		debug = dir(form)
		return render(request, 'distribution/entry.html', {'formset':form, 'range':range(50), 'debug':debug})

@permission_required('distro.auth')
def edit(request):
	date_from = request.GET.get('date_from', '')
	date_until = request.GET.get('date_until', '')
	if date_from:
		date_from = date_from[6:] + '-' + date_from[:2] + '-' + date_from[3:5]
	else:
		date_from = '2013-01-01'
	if date_until:
		date_until = date_until[6:] + '-' + date_until[:2] + '-' + date_until[3:5]
	else:
		date_until = '3013-01-01'
	DistroFormSet = modelformset_factory(Distro, extra=0, can_delete=True)
	#DistroFormSet.date = forms.CharField(widget=TextInput({"class":"datepicker"}))
	if request.method == 'POST':
		formset = DistroFormSet(request.POST)
		if formset.is_valid():
			instances = formset.save()
			queryset = Distro.objects.all()#filter(date__gte=date_from,date__lte=date_until)
			if not request.user.has_perm('distro.uniauth'):
				queryset = queryset.filter(member_organization=request.user.profile_set.get().member_organization)
			form = DistroFormSet(queryset=queryset)
			return render(request, 'distribution/edit.html', {'form':form})
	else:
		
		queryset = Distro.objects.filter(date__gte=date_from).filter(date__lte=date_until)
		
		if not request.user.has_perm('distro.uniauth'):
			queryset = queryset.filter(date__gte=date_from,date__lte=date_until,member_organization=request.user.profile_set.get().member_organization)
		form = DistroFormSet(queryset=queryset.order_by('-date_d'))
		return render(request, 'distribution/edit.html', {'formset':form})

@permission_required('distro.auth')
def download(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=distribution.csv'

	# Create the CSV writer using the HttpResponse as the "file."
	writer = csv.writer(response)
	writer.writerow(['Distribution Date', 'Recipient Site', 'Crops', 'Pounds', 'Containers','Farm', 'Other (notes)', 'Harvest Date', 'Farm Delivery/Field Glean/Farmers Market', 'Pickup/DropOff'])

# date_d = models.DateField("Date of Distribution")
# 	recipient = models.ForeignKey(RecipientSite, verbose_name = "Recipient Site")
# 	crops = models.CharField(max_length=50, blank=True, null=True)
# 	pounds = models.CharField(max_length=5, blank=True, null=True)
# 	containers = models.CharField(max_length=20, blank=True, null=True)
# 	farm = models.ForeignKey(Farm, null=True, blank=True)
# 	other = models.CharField(max_length=50, blank=True, null=True)
# 	date = models.DateField("Date of Harvest")
# 	field_or_farm = models.CharField(max_length=1, choices=g_or_p, default='g')
# 	del_or_pick = models.CharField(max_length=2, choices=d_or_p, default='d')

	if request.user.has_perm('distro.uniauth'):
		group = Distro.objects.all()
	else:
		group = Distro.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	for line in group:
		writer.writerow([
			line.date_d,
			line.recipient,
			line.crops,
			line.pounds,
			line.containers,
			line.farm,
			line.other,
			line.date,
			line.field_or_farm,
			line.del_or_pick,
			])

	return response
# Create your views here.
import time
import datetime
import csv


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
	lines = request.GET.get('extra', 0)
	DistroFormSet = modelformset_factory(Distro, extra=int(lines))
	if request.method == 'POST':
		formset = DistroFormSet(request.POST)
		instances = formset.save(commit=False)
		for instance in instances:
			instance.member_organization = request.user.profile_set.get().member_organization
			instance.save()
		return HttpResponseRedirect(reverse('distro:entry'))
	else:
		form = DistroFormSet(queryset=Distro.objects.none())
		return render(request, 'distribution/entry.html', {'form':form, 'lines':lines})

@permission_required('distro.auth')
def edit(request):
	DistroFormSet = modelformset_factory(Distro, extra=0, can_delete=True)
	date_from = request.GET.get('date_from', datetime.datetime.today())
	date_until = request.GET.get('date_until', datetime.datetime.today())
	if request.method == 'POST':
		formset = DistroFormSet(request.POST)
		if formset.is_valid():
			instances = formset.save()
			queryset = Distro.objects.filter(date__gte=date_from).filter(date__lte=date_until)
			if not request.user.has_perm('distro.uniauth'):
				queryset.filter(member_organization=request.user.profile_set.get().member_organization)
			form = DistroFormSet(queryset=queryset)
			return render(request, 'distribution/edit.html', {'form':form})
	else:
		
		queryset = Distro.objects.filter(date__gte=date_from).filter(date__lte=date_until)
		if not request.user.has_perm('distro.uniauth'):
			queryset.filter(member_organization=request.user.profile_set.get().member_organization)
		form = DistroFormSet(queryset=queryset)
		return render(request, 'distribution/edit.html', {'form':form})

@permission_required('distro.auth')
def download(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=distribution.csv'

	# Create the CSV writer using the HttpResponse as the "file."
	writer = csv.writer(response)
	writer.writerow(['Date', 'Farm', 'Crops', 'Pounds', 'Other', 'Containers', 'Recipient Site', 'Pickup/DropOff', 'Farm Delivery or Field Glean'])

 #    date = models.DateField()
	# farm = models.ForeignKey(Farm, null=True, blank=True)
	# crops = models.CharField(max_length=50, blank=True, null=True)
	# pounds = models.CharField(max_length=5, default=0)
	# other = models.CharField(max_length=50, blank=True, null=True)
	# containers = models.CharField(max_length=20, blank=True, null=True)
	# recipient = models.ForeignKey(Site, verbose_name = "Recipient Site")
	# del_or_pick = models.CharField(max_length=2, choices=d_or_p, default='d')
	# field_or_farm = models.CharField(max_length=1, choices=g_or_p, default='g')

	if request.user.has_perm('distro.uniauth'):
		group = Distro.objects.all()
	else:
		group = Distro.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	for line in group:
		writer.writerow([line.date,
			line.farm,
			line.crops,
			line.pounds,
			line.other,
			line.containers,
			line.recipient,
			line.del_or_pick,
			line.field_or_farm])

	return response
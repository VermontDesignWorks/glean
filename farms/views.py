# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from farms.models import Farm, FarmForm, FarmLocation, LocationForm

#@login_required
def index(request):
	farms_list = Farm.objects.all()
	return render(request, 'farms/index.html', {'farms':farms_list})

#@login_required
def newFarm(request):
	if request.method == "POST":
		form = FarmForm(request.POST)
		if form.is_valid():
			newFarm = Farm(**form.cleaned_data)
			newFarm.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(newFarm.id,) ))
		else:
			return HttpResponse('you totally messed something up')
	else:
		form = FarmForm()
		return render(request, 'farms/new.html', {'form':form})

#@login_required
def editFarm(request, farm_id):
	if request.method == "POST":
		form = FarmForm(request.POST)
		if form.is_valid():
			newFarm = Farm(**form.cleaned_data)
			newFarm.id = farm_id
			newFarm.save()
			return HttpResponseRedirect(reverse('farms:index'))
	farm = get_object_or_404(Farm, pk=farm_id)
	form = FarmForm(instance = farm)

	return render(request, 'farms/edit.html', {'form':form, 'farm':farm})

#@login_required
def detailFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	return render(request, 'farms/detail.html', {'farm':farm})

def newLocation(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.method == 'POST':
		form = LocationForm(request.POST)
		if form.is_valid():
			new_location = FarmLocation(**form.cleaned_data)
			try:
				same_title = FarmLocation.objects.get(name=form.cleaned_data.name)
				return render(request, 'farms/new_location.html', {'form':form, 'farm':farm, 'error':'Already a location by that name'})	
			except:
				new_location.farm = farm
				new_location.save()
				return HttpResponseRedirect(reverse('farms:detailfarm', args=(farm_id,)))

		else:
			return render(request, 'farms/new_location.html', {'form':form, 'farm':farm, 'error':'Form was incorrectly filled out'})
	else:
		form = LocationForm()
		return render(request, 'farms/new_location.html', {'form':form, 'farm':farm})

def editLocation(request, farm_id, location_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	location = get_object_or_404(Farm, pk=location_id)
	if request.method == 'POST':
		pass
	else:
		form = LocationForm(instance = location)
		return renter(request, 'farms/edit_location.html', {'form':form, 'farm':farm})
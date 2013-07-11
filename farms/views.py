# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from farms.models import Farm, FarmForm, FarmLocation, LocationForm, Contact, ContactForm

#@login_required
def index(request):
	farms_list = Farm.objects.all()
	return render(request, 'farms/index.html', {'farms':farms_list})

#@login_required
def newFarm(request):
	if request.method == "POST":
		form = FarmForm(request.POST)
		if form.is_valid():
			#newFarm = Farm(**form.cleaned_data)
			#newFarm.save()
			new_save = form.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(new_save.id,) ))
		else:
			return render(request, 'farms/new.html', {'form':form, 'error':'Your Farm Form Was Not Valid'})
	else:
		form = FarmForm()
		return render(request, 'farms/new.html', {'form':form})

#@login_required
def editFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.method == "POST":
		form = FarmForm(request.POST, instance=farm)
		if form.is_valid():
			#newFarm = Farm(**form.cleaned_data)
			#newFarm.id = farm_id
			#newFarm.save()
			new_save = form.save()
			return HttpResponseRedirect(reverse('farms:index'))
		else:
			return render(request, 'farms/edit.html', {'form':form, 'farm':farm, 'error':'form needs some work', 'editmode':True})
	form = FarmForm(instance = farm)

	return render(request, 'farms/edit.html', {'form':form, 'farm':farm, 'editmode':True})

#@login_required
def detailFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	return render(request, 'farms/detail.html', {'farm':farm})

def newLocation(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.method == 'POST':
		form = LocationForm(request.POST)
		if form.is_valid():
			#new_location = FarmLocation(**form.cleaned_data)
			if not FarmLocation.objects.filter(name=form.cleaned_data['name'], farm=farm).exists():
				#.farm = farm
				#new_location.save()
				new_save = form.save(commit=False)
				new_save .farm=farm
				new_save.save()
				return HttpResponseRedirect(reverse('farms:detailfarm', args=(farm_id,)))
			else:
				return render(request, 'farms/new_location.html', {'form':form, 'farm':farm, 'error':'That Location Name is Taken'})	

		else:
			return render(request, 'farms/new_location.html', {'form':form, 'farm':farm, 'error':'Form was incorrectly filled out'})
	else:
		form = LocationForm()
		return render(request, 'farms/new_location.html', {'form':form, 'farm':farm})

def editLocation(request, farm_id, location_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	location = get_object_or_404(FarmLocation, pk=location_id)
	if request.method == 'POST':
		form = LocationForm(request.POST, instance=location)
		if form.is_valid():
			#new_save = FarmLocation(**form.cleaned_data)
			#new_save.id = location_id
			#new_save.farm = farm
			#new_save.save()
			new_save = form.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(farm_id,)))
		else:
			return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'error':'Form Had an Error', 'editmode':True})
	else:
		form = LocationForm(instance = location)
		return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'editmode':True})

def newContact(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			new_contact = Contact(**form.cleaned_data)
			new_contact.farm = farm
			new_contact.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(farm_id,)))

		else:
			return render(request, 'farms/new_contact.html', {'form':form, 'farm':farm, 'error':'Form was incorrectly filled out'})
	else:
		form = ContactForm()
		return render(request, 'farms/new_contact.html', {'form':form, 'farm':farm})

def editContact(request, farm_id, contact_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	contact = get_object_or_404(Contact, pk=contact_id)
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			new_save = Contact(**form.cleaned_data)
			new_save.id = contact_id
			new_save.farm = farm
			new_save.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(farm_id,)))
		else:
			return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'error':'Form Had an Error','editmode':True})
	else:
		form = ContactForm(instance = contact)
		return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'editmode':True})
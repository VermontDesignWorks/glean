# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from farms.models import Farm, FarmForm, FarmLocation, LocationForm, Contact, ContactForm

@permission_required('farms.auth')
def index(request):
	if request.user.has_perm('farms.uniauth'):
		farms_list = Farm.objects.all().order_by('name')
	else:
		farms_list = Farm.objects.filter(member_organization=request.user.profile_set.get().member_organization).order_by('name')
	return render(request, 'farms/index.html', {'farms':farms_list})

@permission_required('farms.auth')
def newFarm(request):
	if request.method == "POST":
		form = FarmForm(request.POST)
		if form.is_valid():
			#newFarm = Farm(**form.cleaned_data)
			#newFarm.save()
			new_save = form.save()
			new_save.member_organization.add(request.user.profile_set.get().member_organization)
			new_save.save()
			return HttpResponseRedirect(reverse('farms:detailfarm', args=(new_save.id,) ))
		else:
			return render(request, 'farms/new.html', {'form':form, 'error':'Your Farm Form Was Not Valid'})
	else:
		form = FarmForm()
		return render(request, 'farms/new.html', {'form':form})

@permission_required('farms.auth')
def editFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
	if request.method == "POST":
		form = FarmForm(request.POST, instance=farm)
		if form.is_valid():
			new_save = form.save()
			return HttpResponseRedirect(reverse('farms:index'))
		else:
			return render(request, 'farms/edit.html', {'form':form, 'farm':farm, 'error':'form needs some work'})
	form = FarmForm(instance = farm)

	return render(request, 'farms/edit.html', {'form':form, 'farm':farm})

@permission_required('farms.auth')
def detailFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
	return render(request, 'farms/detail.html', {'farm':farm})

#== Delete Farm View ==#
@permission_required('farms.auth')
def deleteFarm(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
	if request.method == 'POST':
		contacts = Contact.objects.filter(farm=farm)
		if contacts.exists():
			for contact in contacts:
				contact.delete()
		locations = FarmLocation.objects.filter(farm=farm)
		if locations.exists():
			for location in locations:
				location.delete()
		farm.delete()
		return HttpResponseRedirect(reverse('farms:index'))
	else:
		return render(request, 'farms/delete_farm.html', {'farm':farm})

@permission_required('farms.auth')
def newLocation(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
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

@permission_required('farms.auth')
def editLocation(request, farm_id, location_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
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
			return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'error':'Form Had an Error'})
	else:
		form = LocationForm(instance = location)
		return render(request, 'farms/edit_location.html', {'form':form, 'farm':farm, 'editmode':True})

@permission_required('farms.auth')
def newContact(request, farm_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
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

@permission_required('farms.auth')
def editContact(request, farm_id, contact_id):
	farm = get_object_or_404(Farm, pk=farm_id)
	if request.user.profile_set.get().member_organization not in farm.member_organization.all() and not request.user.has_perm('farms.uniauth'):
		return HttpResponseRedirect(reverse('farms:index'))
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
			return render(request, 'farms/edit_contact.html', {'form':form, 'farm':farm, 'error':'Form Had an Error'})
	else:
		form = ContactForm(instance = contact)
		return render(request, 'farms/edit_contact.html', {'form':form, 'farm':farm,})
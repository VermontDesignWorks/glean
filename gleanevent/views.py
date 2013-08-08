import time
import datetime
import csv

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.forms.models import modelformset_factory

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from gleanevent.models import GleanEvent, GleanForm, PostGlean# PostGleanForm
from announce.models import Announcement
from functions import primary_address

from django.contrib.comments.forms import CommentForm

class CustomCommentForm(CommentForm):

    def __init__(self, *args, **kwargs):
        super(CustomCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()

@login_required
def index(request):
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
	# if request.user.has_perm('gleanevent.uniauth'):
	gleaning_events_list = GleanEvent.objects.all()
	# else:
	# 	gleaning_events_list = GleanEvent.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	gleaning_events_list = gleaning_events_list.filter(date__gte=date_from).filter(date__lte=date_until)
	return render(request, 'gleanevent/index.html', {'gleans':gleaning_events_list})

@permission_required('gleanevent.auth')
def newGlean(request):
	if request.method == "POST":
		form = GleanForm(request.POST)
		if form.is_valid():
			#newGlean = GleanEvent(**form.cleaned_data)
			#newGlean.save()
			new_save = form.save(commit=False)
			new_save.created_by = request.user
			new_save.member_organization = request.user.profile_set.get().member_organization
			new_save.save()
			form.save_m2m()
			# for county in form.cleaned_data['counties']:
			# 	new_save.counties.add(county)
			# return HttpResponse(new_save.counties.all())
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(new_save.id,) ))
		return HttpResponse('form was not valid')
			
	else:
		form = GleanForm()
		return render(request, 'gleanevent/new.html', {'form':form})

@permission_required('gleanevent.auth')
def editGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if glean.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('gleanevent.uniauth'):
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	if not glean.happened():
		if request.method == "POST":
			form = GleanForm(request.POST, instance = glean)
			
			if form.is_valid():
				new_save = form.save()
				return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(new_save.id,) ))
			else:
				return render(request, 'gleanevent/edit.html', {'form':form, 'glean':glean, 'error':form.errors})
		else:
			form = GleanForm(instance = glean)
			return render(request, 'gleanevent/edit.html', {'form':form, 'glean':glean, 'error':''})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))

@login_required
def detailGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	address = primary_address(glean)
	# if glean.address_one:
	# 	address = glean
	# elif glean.farm_location and glean.farm_location.address_one:
	# 	address = glean.farm_location
	# elif glean.farm and glean.farm.address_one:
	# 	address = glean.farm
	# else:
	# 	address = None
	#return HttpResponse()
	return render(request, 'gleanevent/detail.html', {'glean':glean,'address':address})

#== Delete Glean View ==#
@permission_required('gleanevent.auth')
def deleteGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if glean.member_organization != request.user.profile_set.get().member_organization and u'gleanevent.uniauth' not in request.user.groups.get().permissions.all():
		return HttpResponseRedirect(reverse('gleanevent:index'))
	if request.method == 'POST':
		announces = Announcement.objects.filter(glean=glean)
		if announces.exists():
			for announce in announces:
				announce.delete()
		glean.delete()
		return HttpResponseRedirect(reverse('gleanevent:index'))
	else:
		return render(request, 'gleanevent/delete.html', {'glean':glean})

@login_required
def confirmLink(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if not glean.happened():
		if request.user not in glean.rsvped.all():
			glean.rsvped.add(request.user)
			profile = request.user.profile_set.get()
			profile.rsvped += 1
			profile.save()
			if request.user not in glean.member_organization.volunteers.all():
				glean.member_organization.volunteers.add(request.user)
			if request.user in glean.not_rsvped.all():
				glean.not_rsvped.remove(request.user)
			glean.save()
		return render(request, 'gleanevent/confirm.html', {'glean':glean})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))

@login_required
def denyLink(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if not glean.happened():
		if request.user not in glean.not_rsvped.all():
			glean.not_rsvped.add(request.user)
			if request.user in glean.rsvped.all():
				glean.rsvped.remove(request.user)
				profile = request.user.profile_set.get()
				profile.rsvped -= 1
				profile.save()
			glean.save()
			return render(request, 'gleanevent/deny.html', {'glean':glean})
		else:
			if request.user in glean.rsvped.all():
				glean.rsvped.remove(request.user)
			return render(request, 'gleanevent/deny.html', {'glean':glean})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))

@permission_required('gleanevent.auth')
def postGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if glean.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('gleanevent.uniauth'):#u'gleanevent.uniauth' not in request.user.groups.get().permissions.all():
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	#if not glean.data_entered() and glean.happened():
	count = len(glean.rsvped.all())
	unrsvped = int(request.GET.get('extra', 0))
	if int(unrsvped) > 100:
		unrsvped = 100
	PostGleanFormSet = modelformset_factory(PostGlean, extra=count+unrsvped)
	#formset = PostGleanFormSet(queryset=PostGlean.objects.none())
	
	if request.method == 'POST':
		formset = PostGleanFormSet(request.POST)
		instances = formset.save(commit=False)
		for i in range(count):
			instances[i].glean= glean
			instances[i].user = glean.rsvped.all()[i]
			if instances[i].attended == True:
				profile = instances[i].user.profile_set.get()
				profile.attended += 1
				if instances[i].hours:
					profile.hours += instances[i].hours
				profile.save()
		for instance in instances:
			if not hasattr(instance, 'glean'):
				instance.glean = glean
			instance.save()
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	else:
		initial = []
		for person in glean.rsvped.all():
			prof = person.profile_set.get()
			initial.append({'first_name':prof.first_name,
							'last_name':prof.last_name})
		#return HttpResponse(str(initial))
		forms=PostGleanFormSet(initial=initial, queryset=PostGlean.objects.none())
		return render(request, 'gleanevent/postglean.html', {'glean':glean, 'formset':forms})
	#else:
	#		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))


def postGleanView(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	glean_data = PostGlean.objects.filter(glean=glean)
	return render(request, 'gleanevent/post_glean.html', {'glean':glean, 'glean_data':glean_data})

def postGleanEdit(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	PostGleanFormSet = modelformset_factory(PostGlean, extra=0, can_delete=True)
	if request.method == 'POST':
		formset = PostGleanFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return HttpResponseRedirect(reverse('gleanevent:postgleanview', args=(glean_id,)))

	forms = PostGleanFormSet(queryset=PostGlean.objects.filter(glean=glean))

	return render(request, 'gleanevent/postgleanedit.html', {'glean':glean, 'formset':forms})

@permission_required('gleanevent.auth')
def printGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	return render(request, 'gleanevent/print.html', {'glean':glean})

@permission_required('gleanevent.auth')
def download(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=gleanevent.csv'

	# Create the CSV writer using the HttpResponse as the "file."
	writer = csv.writer(response)
	writer.writerow([
			'title',
			'address_one',
			'address_two',
			'city',
			'state',

			'date',
			'time',
			'description',
			'crops',

			'directions',
			'instructions',

			'volunteers_needed',
			'duration',

			'farm',
			'farm_location',

			'created_by',
			'invited_volunteers',

			'rsvped',
			'not_rsvped',
			'waitlist',

			'attending_volunteers',
			'officiated_by',
			'counties',

			'member_organization',
	])

	if request.user.has_perm('gleanevent.uniauth'):
		gleans = GleanEvent.objects.all()
	else:
		gleans = GleanEvent.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	for glean in gleans:
		writer.writerow([
			glean.title,
			glean.address_one,
			glean.address_two,
			glean.city,
			glean.state,

			glean.date,
			glean.time,
			glean.description,
			glean.crops,

			glean.directions,
			glean.instructions,

			glean.volunteers_needed,
			glean.duration,

			glean.farm,
			glean.farm_location,

			glean.created_by,
			glean.invited_volunteers.all(),

			glean.rsvped.all(),
			glean.not_rsvped.all(),
			glean.waitlist.all(),

			glean.attending_volunteers.all(),
			glean.officiated_by.all(),
			glean.counties.all(),

			glean.member_organization,
			])

	return response

@permission_required('gleanevent.auth')
def postGleanDownload(request):
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=postglean.csv'

	# Create the CSV writer using the HttpResponse as the "file."
	writer = csv.writer(response)
	writer.writerow([
			'glean',
			'user',
			'attended',
			'first_name',
			'last_name',
			'hours',
			'group',
			'members',
			'notes',
	])

	if request.user.has_perm('gleanevent.uniauth'):
		postgleans = PostGlean.objects.all()
	else:
		postgleans = PostGlean.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	for postglean in postgleans:
		writer.writerow([
			postglean.glean,
			postglean.user,
			postglean.attended,
			postglean.first_name,
			postglean.last_name,
			postglean.hours,
			postglean.group,
			postglean.members,
			postglean.notes,
			])

	return response

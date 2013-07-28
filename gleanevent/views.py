import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from django.contrib.auth.decorators import permission_required

from gleanevent.models import GleanEvent, GleanForm, PostGlean# PostGleanForm

@permission_required('gleanevent.auth')
def index(request):
	if request.user.has_perm('gleanevent.uniauth'):
		gleaning_events_list = GleanEvent.objects.all()
	else:
		gleaning_events_list = GleanEvent.objects.filter(member_organization=request.user.profile_set.get().member_organization)
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
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(new_save.id,) ))
		return HttpResponse('form was not valid')
			
	else:
		form = GleanForm()
		return render(request, 'gleanevent/new.html', {'form':form})

@permission_required('gleanevent.auth')
def editGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if glean.member_organization != request.user.profile_set.get().member_organization and u'gleanevent.uniauth' not in request.user.groups.get().permissions.all():
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	if not glean.happened():
		if request.method == "POST":
			form = GleanForm(request.POST, instance = glean)
			#return HttpResponse('texst2')
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
	return render(request, 'gleanevent/detail.html', {'glean':glean})

# def gleanCalendar(request):
# 	gleans = GleanEvent.objects.all()
# 	return render(request, 'gleanevent/calendar.html', {'gleans':gleans})

# def announceGlean(request, glean_id):
# 	glean = get_object_or_404(GleanEvent, pk=glean_id)
# 	return render(request, 'gleanevent/announce.html', {'glean':glean})

@login_required
def confirmLink(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if not glean.happened():
		if request.user not in glean.rsvped.all():
			glean.rsvped.add(request.user)
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
			glean.save()
		return render(request, 'gleanevent/deny.html', {'glean':glean})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))

@permission_required('gleanevent.auth')
def postGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if glean.member_organization != request.user.profile_set.get().member_organization and u'gleanevent.uniauth' not in request.user.groups.get().permissions.all():
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	if not glean.data_entered() and glean.happened():
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
				#instances[i].save()
			for instance in instances:
				if not hasattr(instance, 'glean'):
					instance.glean = glean
				instance.save()
			return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
		else:
			#formset = PostGleanFormSet(queryset=PostGlean.objects.none())
			initial = []
			for person in glean.rsvped.all():
				prof = person.profile_set.get()
				initial.append({'first_name':prof.first_name,
								'last_name':prof.last_name})
			#return HttpResponse(str(initial))
			forms=PostGleanFormSet(initial=initial, queryset=PostGlean.objects.none())
			return render(request, 'gleanevent/postglean.html', {'glean':glean, 'forms':forms})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
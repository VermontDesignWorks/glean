# Create your views here.
import time
import datetime


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

from distro.models import Distro

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
	
	# 	count = len(glean.rsvped.all())
	# 	unrsvped = int(request.GET.get('extra', 0))
	# 	if int(unrsvped) > 100:
	# 		unrsvped = 100
	# 	PostGleanFormSet = modelformset_factory(PostGlean, extra=count+unrsvped)
	# 	#formset = PostGleanFormSet(queryset=PostGlean.objects.none())
		
	# 	if request.method == 'POST':
	# 		formset = PostGleanFormSet(request.POST)
	# 		instances = formset.save(commit=False)
	# 		for i in range(count):
	# 			instances[i].glean= glean
	# 			instances[i].user = glean.rsvped.all()[i]
	# 			#instances[i].save()
	# 		for instance in instances:
	# 			if not hasattr(instance, 'glean'):
	# 				instance.glean = glean
	# 			instance.save()
	# 		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	# 	else:
	# 		#formset = PostGleanFormSet(queryset=PostGlean.objects.none())
	# 		initial = []
	# 		for person in glean.rsvped.all():
	# 			prof = person.profile_set.get()
	# 			initial.append({'first_name':prof.first_name,
	# 							'last_name':prof.last_name})
	# 		#return HttpResponse(str(initial))
	# 		forms=PostGleanFormSet(initial=initial, queryset=PostGlean.objects.none())
	# 		return render(request, 'gleanevent/postglean.html', {'glean':glean, 'forms':forms})
	# else:
	# 	return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
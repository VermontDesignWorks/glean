# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from counties.models import County, CountyForm


def index(request):
	counties_list = County.objects.all()
	return render(request, 'counties/index.html', {'counties':counties_list})

#@login_required
def newCounty(request):
	if request.method == "POST":
		form = CountyForm(request.POST)
		if form.is_valid():
			new_save = County(**form.cleaned_data)
			new_save.save()
			return HttpResponseRedirect(reverse('counties:detailcounty', args=(new_save.id,) ))
		else:
			return render(request, 'counties/new_county.html', {'form':form, 'error':'Your County Form Was Not Valid'})
	else:
		form = CountyForm()
		return render(request, 'counties/new_county.html', {'form':form})

#@login_required
def editCounty(request, county_id):
	county = get_object_or_404(County, pk=county_id)
	if request.method == "POST":
		form = CountyForm(request.POST)
		if form.is_valid():
			new_save = County(**form.cleaned_data)
			new_save.id = county_id
			new_save.save()
			return HttpResponseRedirect(reverse('counties:index'))
		else:
			return render(request, 'counties/edit_county.html', {'form':form, 'county':county, 'error':'form needs some work', 'editmode':True})
	form = CountyForm(instance = county)

	return render(request, 'counties/edit_county.html', {'form':form, 'county':county, 'editmode':True})

def detailCounty(request, county_id):
	county = get_object_or_404(County, pk=county_id)
	return render(request, 'counties/detail_county.html', {'county':county})
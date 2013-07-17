# Create your views here.
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from recipientsite.models import Site, SiteForm


def index(request):
	sites_list = Site.objects.all()
	return render(request, 'recipientsite/index.html', {'sites':sites_list})

#@login_required
def newSite(request):
	if request.method == "POST":
		form = SiteForm(request.POST)
		if form.is_valid():
			new_save = Site(**form.cleaned_data)
			new_save.save()
			return HttpResponseRedirect(reverse('site:detailsite', args=(new_save.id,) ))
		else:
			return render(request, 'recipientsite/new_site.html')
	else:
		form = SiteForm()
		return render(request, 'recipientsite/new_site.html', {'form':form})

#@login_required
def editSite(request, site_id):
	site = get_object_or_404(Site, pk=site_id)
	if request.method == "POST":
		form = SiteForm(request.POST)
		if form.is_valid():
			new_save = Site(**form.cleaned_data)
			new_save.id = site_id
			new_save.save()
			return HttpResponseRedirect(reverse('site:index'))
		else:
			return render(request, 'recipientsite/edit_site.html', {'form':form, 'site':site, 'error':'form needs some work', 'editmode':True})
	form = SiteForm(instance = site)

	return render(request, 'recipientsite/edit_site.html', {'form':form, 'site':site, 'editmode':True})

def detailSite(request, site_id):
	site = get_object_or_404(Site, pk=site_id)
	return render(request, 'recipientsite/detail_site.html', {'site':site})
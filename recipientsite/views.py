# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import permission_required

from recipientsite.models import RecipientSite, SiteForm

@permission_required('recipientsite.auth')
def index(request):
	if request.user.has_perm('recipientsite.uniauth'):
		sites_list = RecipientSite.objects.all()
	else:
		sites_list = RecipientSite.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	return render(request, 'recipientsite/index.html', {'sites':sites_list})

@permission_required('recipientsite.auth')
def newSite(request):
	if request.method == "POST":
		form = SiteForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.member_organization = request.user.profile_set.get().member_organization
			new_save.save()
			return HttpResponseRedirect(reverse('site:detailsite', args=(new_save.id,) ))
		else:
			return render(request, 'recipientsite/new_site.html')
	else:
		form = SiteForm()
		return render(request, 'recipientsite/new_site.html', {'form':form})

@permission_required('recipientsite.auth')
def editSite(request, site_id):
	site = get_object_or_404(RecipientSite, pk=site_id)
	if site.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('recipientsite.uniauth'):
		return HttpResponseRedirect(reverse('site:index'))
	if request.method == "POST":
		form = SiteForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.id = site_id
			new_save.member_organization = site.member_organization
			new_save.save()
			return HttpResponseRedirect(reverse('site:index'))
		else:
			return render(request, 'recipientsite/edit_site.html', {'form':form, 'site':site, 'error':'form needs some work', 'editmode':True})
	form = SiteForm(instance = site)

	return render(request, 'recipientsite/edit_site.html', {'form':form, 'site':site, 'editmode':True})

@permission_required('recipientsite.auth')
def detailSite(request, site_id):
	site = get_object_or_404(RecipientSite, pk=site_id)
	if site.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('recipientsite.uniauth'):
		return HttpResponseRedirect(reverse('site:index'))
	return render(request, 'recipientsite/detail_site.html', {'site':site})

#== Delete RecipientSite View ==#
@permission_required('recipientsite.auth')
def deleteSite(request, site_id):
	site = get_object_or_404(RecipientSite, pk=site_id)
	if site.member_organization != request.user.profile_set.get().member_organization and not request.user.has_perm('recipientsite.uniauth'):
		return HttpResponseRedirect(reverse('site:index'))
	if request.method == 'POST':
		site.delete()
		return HttpResponseRedirect(reverse('site:index'))
	else:
		return render(request, 'recipientsite/delete_site.html', {'site':site})
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic.detail import DetailView
from recipientsite.models import RecipientSite, SiteForm
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from generic.mixins import SimpleLoginCheckForGenerics
from recipientsite.forms import RecipientSiteForm


@permission_required('recipientsite.auth')
def index(request):
    if request.user.has_perm('recipientsite.uniauth'):
        sites_list = RecipientSite.objects.all().order_by('member_organization', 'name')
    else:
        sites_list = RecipientSite.objects.filter(member_organization=request.user.profile.member_organization).order_by('name')
    return render(request, 'recipientsite/index.html', {'sites':sites_list})


class NewSite(CreateView):
    model = RecipientSite
    template_name = 'recipientsite/new_site.html'
    form_class = RecipientSiteForm
    success_url = reverse_lazy('site:index')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        new_save = form.save(commit=False)
        memorg = self.request.user.profile.member_organization
        new_save.member_organization = memorg
        new_save.save()
        return super(NewSite, self).form_valid(form)


class EditSite(UpdateView):
    model = RecipientSite
    template_name = 'recipientsite/edit_site.html'
    form_class = RecipientSiteForm
    success_url = reverse_lazy('site:index')


class DeleteSite(DeleteView):
    model = RecipientSite
    template_name = 'recipientsite/delete_site.html'
    success_url = reverse_lazy('site:index')


class DetailSite(DetailView):
    model = RecipientSite
    template_name = 'recipientsite/detail_site.html'
    success_url = reverse_lazy('site:index')


@permission_required('recipientsite.auth')
def newSite(request):
    if request.method == "POST":
        form = SiteForm(request.POST)
        if form.is_valid():
            new_save = form.save(commit=False)
            new_save.member_organization = request.user.profile.member_organization
            new_save.save()
            if request.POST['action'] == 'Save':
                return HttpResponseRedirect(reverse('site:detailsite', args=(new_save.id,)))
            else:
                form = SiteForm()
                notice = "Recipient Site %s Saved" % (new_save.name)
                return render(request, 'recipientsite/new_site.html', {'form':form, 'notice':notice})
        else:
            return render(request, 'recipientsite/new_site.html', {'form':form})
    else:
        form = SiteForm()
        return render(request, 'recipientsite/new_site.html', {'form':form})


@permission_required('recipientsite.auth')
def editSite(request, site_id):
    site = get_object_or_404(RecipientSite, pk=site_id)
    if site.member_organization != request.user.profile.member_organization and not request.user.has_perm('recipientsite.uniauth'):
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
    form = SiteForm(instance=site)

    return render(request, 'recipientsite/edit_site.html', {'form':form, 'site':site, 'editmode':True})


@permission_required('recipientsite.auth')
def detailSite(request, site_id):
    site = get_object_or_404(RecipientSite, pk=site_id)
    if site.member_organization != request.user.profile.member_organization and not request.user.has_perm('recipientsite.uniauth'):
        return HttpResponseRedirect(reverse('site:index'))
    return render(request, 'recipientsite/detail_site.html', {'site':site})


# == Delete RecipientSite View ==#
@permission_required('recipientsite.auth')
def deleteSite(request, site_id):
    site = get_object_or_404(RecipientSite, pk=site_id)
    if site.member_organization != request.user.profile.member_organization and not request.user.has_perm('recipientsite.uniauth'):
        return HttpResponseRedirect(reverse('site:index'))
    if request.method == 'POST':
        site.delete()
        return HttpResponseRedirect(reverse('site:index'))
    else:
        return render(request, 'recipientsite/delete_site.html', {'site':site})

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
import re


@permission_required('recipientsite.auth')
def index(request):
    if request.user.has_perm('recipientsite.uniauth'):
        sites_list = RecipientSite.objects.all().order_by('member_organization', 'name')
    else:
        sites_list = RecipientSite.objects.filter(member_organization=request.user.profile.member_organization).order_by('name')
    return render(request, 'recipientsite/index.html', {'sites':sites_list})


class NewSite(SimpleLoginCheckForGenerics, CreateView):
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

    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('recipientsite.auth'):
            return super(NewSite, self).dispatch(*args, **kwargs)
        else:
            raise Http404


class EditSite(SimpleLoginCheckForGenerics, UpdateView):
    model = RecipientSite
    template_name = 'recipientsite/edit_site.html'
    form_class = RecipientSiteForm
    success_url = reverse_lazy('site:index')

    def dispatch(self, *args, **kwargs):
        text = re.search('/recipientsite/(.+?)/edit/', self.request.path)
        pk = int(text.group(1))
        site = RecipientSite.objects.get(pk=pk)
        morg = self.request.user.profile.member_organization
        rmo = site.member_organization
        if self.request.user.has_perm('recipientsite.uniauth'):
            return super(EditSite, self).dispatch(*args, **kwargs)
        elif self.request.user.has_perm('recipientsite.auth') and morg == rmo:
            return super(EditSite, self).dispatch(*args, **kwargs)
        else:
            raise Http404


class DeleteSite(SimpleLoginCheckForGenerics, DeleteView):
    model = RecipientSite
    template_name = 'recipientsite/delete_site.html'
    success_url = reverse_lazy('site:index')

    def dispatch(self, *args, **kwargs):
        text = re.search('/recipientsite/(.+?)/delete/', self.request.path)
        pk = int(text.group(1))
        site = RecipientSite.objects.get(pk=pk)
        morg = self.request.user.profile.member_organization
        rmo = site.member_organization
        if self.request.user.has_perm('recipientsite.uniauth'):
            return super(DeleteSite, self).dispatch(*args, **kwargs)
        elif self.request.user.has_perm('recipientsite.auth') and morg == rmo:
            return super(DeleteSite, self).dispatch(*args, **kwargs)
        else:
            raise Http404


class DetailSite(SimpleLoginCheckForGenerics, DetailView):
    model = RecipientSite
    template_name = 'recipientsite/detail_site.html'
    success_url = reverse_lazy('site:index')

    def dispatch(self, *args, **kwargs):
        text = re.search('/recipientsite/(.+?)/', self.request.path)
        pk = int(text.group(1))
        site = RecipientSite.objects.get(pk=pk)
        morg = self.request.user.profile.member_organization
        rmo = site.member_organization
        if self.request.user.has_perm('recipientsite.uniauth'):
            return super(DetailSite, self).dispatch(*args, **kwargs)
        elif self.request.user.has_perm('recipientsite.auth') and morg == rmo:
            return super(DetailSite, self).dispatch(*args, **kwargs)
        else:
            raise Http404

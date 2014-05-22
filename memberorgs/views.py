from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.models import User, Group

from constants import TRUNCATED_LEVELS

from userprofile.models import Profile
from memberorgs.models import MemOrg, MemOrgForm, NewAdminForm
from announce.models import Template

from django.views import generic

from generic.mixins import SimpleLoginCheckForGenerics

from memberorgs.forms import *

from django.http import Http404


@permission_required('memberorgs.auth')
def index(request):
    if request.user.has_perm('memberorgs.uniauth'):
        memorgs_list = MemOrg.objects.all().order_by('name')
    else:
        memorg_id = request.user.profile.member_organization.id
        return HttpResponseRedirect(
            reverse('memorgs:detailmemorg', args=(memorg_id,)))
    return render(request, 'memberorgs/index.html', {'memorgs': memorgs_list})


class NewMemOrg(SimpleLoginCheckForGenerics, generic.CreateView):
    template_name = "memberorgs/new_memorg.html"
    form_class = NewMemOrgForm
    model = MemOrg
    success_url = reverse_lazy("home")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.has_perm('memberorgs.uniauth'):
            return super(NewMemOrg, self).dispatch(*args, **kwargs)
        else:
            raise Http404
            return self.http_method_not_allowed(
                self.request, *args, **kwargs)


class EditMemOrg(generic.UpdateView):
    template_name = "memberorgs/edit_memorg.html"
    model = MemOrg
    form_class = MemOrgForm
    success_url = reverse_lazy(
        'memorgs:detailmemorg')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.kwargs["pk"].isdigit:
            if int(self.request.user.profile.member_organization.pk) == int(
                    self.kwargs["pk"]):
                return super(EditMemOrg, self).dispatch(*args, **kwargs)
            elif self.request.user.has_perm('memberorgs.uniauth'):
                return super(EditMemOrg, self).dispatch(*args, **kwargs)
            else:
                return self.http_method_not_allowed(
                    self.request, *args, **kwargs)
        else:
            return self.http_method_not_allowed(self.request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.has_perm('memberorgs.uniauth'):
            return AdminMemOrgForm
        else:
            return MemOrgForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(
            'memorgs:detailmemorg',
            args=[self.kwargs["pk"]])


class DetailMemOrg(generic.DetailView):
    model = MemOrg
    template_name = "memberorgs/detail_memorg.html"


@permission_required('memberorgs.auth')
@permission_required('userprofile.promote')
def newAdministrator(request, memorg_id):
    member_organization = get_object_or_404(MemOrg, pk=memorg_id)
    profile = request.user.profile
    if not request.user.has_perm('memberorgs.uniauth') and (
            member_organization != profile.member_organization):
        return HttpResponseRedirect(
            reverse('memorgs:detailmemorg', args=(memorg_id,)))
    if request.method == 'POST':
        form = NewAdminForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'],
                form.cleaned_data['password'])
            new_profile = Profile(user=new_user,
                                  first_name=form.cleaned_data['first_name'],
                                  last_name=form.cleaned_data['last_name'],
                                  phone=form.cleaned_data['phone'],
                                  member_organization=form.cleaned_data[
                                      'member_organization']
                                  )
            new_profile.save()
            for county in member_organization.counties.all():
                new_profile.counties.add(county)
            if member_organization.name == 'Salvation Farms':
                if form.cleaned_data['access_level'] == 'PD':
                    sal = Group.objects.get(
                        name="Salvation Farms Administrator")
                    new_user.groups.add(sal)
                else:
                    salc = Group.objects.get(
                        name="Salvation Farms Coordinator")
                    new_user.groups.add(salc)
            else:
                if form.cleaned_data['access_level'] == 'PD':
                    ed = Group.objects.get(
                        name="Member Organization Executive Director")
                    new_user.groups.add(ed)
                else:
                    memc = Group.objects.get(
                        name="Member Organization Glean Coordinator")
                    new_user.groups.add(memc)

            if request.POST['action'] == 'Save':
                return HttpResponseRedirect(
                    reverse('memorgs:detailmemorg', args=(memorg_id,)))
            else:
                form = NewAdminForm()
                if not request.user.has_perm('userprofile.uniauth'):
                    form.fields['access_level'].choices = TRUNCATED_LEVELS
                form.fields['member_organization'].queryset = (
                    MemOrg.objects.filter(pk=memorg_id))
                notice = 'Administrator account ' + new_user.username + ''
                ' has been created'
                return render(request, 'memberorgs/newadmin.html',
                              {'form': form, 'notice': notice})
        else:
            return HttpResponse('form.is_not_valid :(')

    form = NewAdminForm()
    form.fields['member_organization'].queryset = MemOrg.objects.filter(
        pk=memorg_id)
    if not request.user.has_perm('userprofile.uniauth'):
        form.fields['access_level'].choices = TRUNCATED_LEVELS
    return render(request, 'memberorgs/newadmin.html', {'form': form})

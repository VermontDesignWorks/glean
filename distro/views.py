# Create your views here.
import csv
import datetime
import time
import sys

from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.forms.models import modelformset_factory, formset_factory
from django.forms.widgets import TextInput
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from extra_views import ModelFormSetView, FormSetView
import tablib

from distro.forms import (WorkEventFormHelper,
                          WorkEventFormSet,
                          EditWorkEventFormSet,
                          )
from distro.models import Distro, WorkEvent
from memberorgs.models import MemOrg
from farms.models import Farm
from generic.views import DateFilterMixin
from recipientsite.models import RecipientSite
from generic.mixins import SimpleLoginCheckForGenerics, DynamicDateFilterMixin
from recipientsite.models import RecipientSite


@permission_required('distro.auth')
def index(request):
    date_from = request.GET.get('date_from', '')
    date_until = request.GET.get('date_until', '')
    profile = request.user.profile
    if date_from:
        date_from = date_from[6:] + '-' + date_from[:2] + '-' + date_from[3:5]
    else:
        date_from = '2013-01-01'
    if date_until:
        date_until = date_until[
            6:] + '-' + date_until[:2] + '-' + date_until[3:5]
    else:
        date_until = '3013-01-01'
    if request.user.has_perm('distro.uniauth'):
        try:
            data = Distro.objects.filter(
                date_d__gte=date_from,
                date_d__lte=date_until
            ).order_by('-date_d')[:30]
            notice = ''
        except:
            data = Distro.objects.all().order_by('-date_d')[:30]
            notice = 'Use the Date Picker, you Muppets!'
    else:
        try:
            data = Distro.objects.filter(
                member_organization=profile.member_organization,
                date_d__gte=date_from,
                date_d__lte=date_until,
            ).order_by('-date_d')[:25]
            notice = ''
        except:
            data = Distro.objects.filter(
                member_organization=profile.member_organization
            ).order_by('-date_d')[:30]
            notice = 'Use the Date Picker, you Muppets!'
    return render(
        request,
        'distribution/index.html',
        {'data': data, 'notice': notice}
    )


class Entry(SimpleLoginCheckForGenerics, ModelFormSetView):

    template_name = 'distribution/entry.html'
    success_url = reverse_lazy("distro:entry")
    extra = 10
    model = Distro
    queryset = Distro.objects.none()

    def construct_formset(self):
        formset = super(Entry, self).construct_formset()
        memorg = self.request.user.profile.member_organization
        permission = 'distro.uniauth'
        for i in range(0, len(formset)):
            for f in formset[i].fields:
                formset[i].fields[f].label = ""
            if not self.request.user.has_perm(permission):
                formset[i].fields[
                    'recipient'
                ].queryset = RecipientSite.objects.filter(
                    member_organization=memorg)
                formset[i].fields[
                    'farm'
                ].queryset = Farm.objects.filter(member_organization=memorg)
                formset[i].fields[
                    'member_organization'
                ].queryset = MemOrg.objects.filter(pk=memorg.pk)
                formset[i].fields[
                    'member_organization'
                ].initial = MemOrg.objects.get(pk=memorg.pk)
                formset[i].fields[
                    'member_organization'
                ].widget = forms.HiddenInput()
        return formset

    def formset_valid(self, form):
        count = 0
        for f in form.forms:
            if f.has_changed():
                count += 1
        messages.add_message(
            self.request,
            messages.INFO,
            "{0} New Item(s) saved to the database".format(count)
        )
        return super(Entry, self).formset_valid(form)


class Edit(DynamicDateFilterMixin,
           SimpleLoginCheckForGenerics,
           ModelFormSetView):

    template_name = 'distribution/edit.html'
    success_url = reverse_lazy("distro:entry")
    model = Distro
    can_delete = True
    can_order = False
    extra = 0
    queryset = Distro.objects.all()
    uniauth_string = "distro.uniauth"

    def construct_formset(self):
        formset = super(Edit, self).construct_formset()
        memorg = self.request.user.profile.member_organization
        permission = 'distro.uniauth'
        for i in range(0, len(formset)):
            for f in formset[i].fields:
                formset[i].fields[f].label = ""
            if not self.request.user.has_perm(permission):
                formset[i].fields[
                    'recipient'
                ].queryset = RecipientSite.objects.filter(
                    member_organization=memorg)
                formset[i].fields[
                    'farm'
                ].queryset = Farm.objects.filter(member_organization=memorg)
                formset[i].fields[
                    'member_organization'
                ].queryset = MemOrg.objects.filter(pk=memorg.pk)
                formset[i].fields[
                    'member_organization'
                ].initial = MemOrg.objects.get(pk=memorg.pk)
                formset[i].fields[
                    'member_organization'
                ].widget = forms.HiddenInput()
        return formset


@permission_required('distro.auth')
def download(request):
    request.POST
    mo = request.user.profile.member_organization
    response = HttpResponse(mimetype='application/xlsx')
    response['Content-Disposition'] = 'attachment; filename=distribution.xlsx'

    # Create the CSV writer using the HttpResponse as the "file."
    headings = [
        'Distribution Date',
        'Recipient Site',
        'Crops',
        'Pounds',
        'Containers',
        'Farm',
        'Other (notes)',
        'Harvest Date',
        'Farm Delivery/Field Glean/Farmers Market',
        'Pickup/DropOff'
    ]
    attributes = [
        'date_d',
        'recipient',
        'crops',
        'pounds',
        'containers',
        'farm',
        'other',
        'date',
        'field_or_farm',
        'del_or_pick'
    ]

    if request.user.has_perm('distro.uniauth'):
        query = Distro.objects.all()
        headings = ["Member Organization"] + headings
        attributes = ['member_organization'] + attributes
    else:
        query = Distro.objects.filter(member_organization=mo)
    params = {}
    if "date_from" in request.GET and request.GET["date_from"]:
        params["date_d__gte"] = datetime.datetime.strptime(
            request.GET["date_from"], "%Y-%m-%d")
    if "date_until" in request.GET and request.GET["date_until"]:
        params["date_d__lte"] = datetime.datetime.strptime(
            request.GET["date_until"], "%Y-%m-%d")
    if params:
        query = query.filter(**params)

    data = tablib.Dataset(headers=headings)

    for distro in query:
        data.append([getattr(distro, attr, "") for attr in attributes])
    response.write(data.xlsx)

    return response


class Hours_Entry(DynamicDateFilterMixin,
                  SimpleLoginCheckForGenerics,
                  ModelFormSetView):

    template_name = 'distribution/hours_create.html'
    success_url = reverse_lazy("distro:hours")
    extra = 10
    model = WorkEvent
    queryset = WorkEvent.objects.all()
    uniauth_string = 'userprofile.uniauth'

    def construct_formset(self):
        formset = super(Hours_Entry, self).construct_formset()
        for i in range(0, len(formset)):
            for f in formset[i].fields:
                formset[i].fields[f].label = ""
        formset.helper = WorkEventFormHelper()
        return formset

    def get_queryset(self):
        if self.request.method == 'post':
            self.extra = 0
            return super(Hours_Entry, self).get_queryset()
        else:
            GET = self.request.GET
            if "date_from" in GET or "date_until" in GET:
                self.extra = 0
                return super(Hours_Entry, self).get_queryset()
            else:
                queryset = WorkEvent.objects.none()
                self.extra = 10
                return queryset

    def formset_valid(self, formset):
        memorg = self.request.user.profile.member_organization
        self.object_list = formset.save(commit=False)
        for instance in self.object_list:
            instance.member_organization = memorg
            instance.save()
        return HttpResponseRedirect(self.get_success_url())

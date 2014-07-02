# Create your views here.
import csv
import datetime
import time
import sys

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.forms.models import modelformset_factory, formset_factory
from django.forms.widgets import TextInput
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from extra_views import ModelFormSetView, FormSetView

from distro.forms import (WorkEventFormHelper,
                          WorkEventFormSet,
                          EditWorkEventFormSet,
                          DistroEntryForm,
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
    success_url = reverse_lazy("distro:index")
    # form_class = DistroEntryForm
    extra = 10
    model = Distro
    queryset = Distro.objects.none()

    def construct_formset(self):
        formset = super(Entry, self).construct_formset()
        memorg = self.request.user.profile.member_organization
        permission = 'distro.uniauth'
        if not self.request.user.has_perm(permission):
            for i in range(0, len(formset)):
                for f in formset[i].fields:
                    formset[i].fields[f].label = ""
                formset[i].fields['recipient'].queryset = RecipientSite.objects.filter(member_organization=memorg)
                formset[i].fields['farm'].queryset = Farm.objects.filter(member_organization=memorg)
                formset[i].fields['member_organization'].queryset = MemOrg.objects.filter(pk=memorg.pk)
                formset[i].fields['member_organization'].widget = forms.HiddenInput()
                formset[i].fields['member_organization'].initial = MemOrg.objects.get(pk=memorg.pk)
        return formset


class Edit(DynamicDateFilterMixin, SimpleLoginCheckForGenerics, ModelFormSetView):

    template_name = 'distribution/edit.html'
    success_url = reverse_lazy("distro:index")
    #form_class = DistroEntryForm
    model = Distro
    can_delete = True
    can_order = False
    extra = 0
    queryset = Distro.objects.all()

    def construct_formset(self):
        formset = super(Edit, self).construct_formset()
        memorg = self.request.user.profile.member_organization
        permission = 'distro.uniauth'
        if not self.request.user.has_perm(permission):
            for i in range(0, len(formset)):
                for f in formset[i].fields:
                    formset[i].fields[f].label = ""
                formset[i].fields['recipient'].queryset = RecipientSite.objects.filter(member_organization=memorg)
                formset[i].fields['farm'].queryset = Farm.objects.filter(member_organization=memorg)
                formset[i].fields['member_organization'].queryset = MemOrg.objects.filter(pk=memorg.pk)
                formset[i].fields['member_organization'].widget = forms.HiddenInput()
                formset[i].fields['member_organization'].initial = MemOrg.objects.get(pk=memorg.pk)
        return formset


@permission_required('distro.auth')
def download(request):
    mo = request.user.profile.member_organization
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=distribution.csv'

    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)

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
        group = Distro.objects.all()
        headings = ["Member Organization"] + headings
        attributes = ['member_organization'] + attributes
    else:
        group = Distro.objects.filter(member_organization=mo)

    writer.writerow(headings)

    for line in group:
        writer.writerow([getattr(line, attr, "") for attr in attributes])

    return response


@permission_required('distro.auth')
def hours_entry(request):
    member_organization = request.user.profile.member_organization
    if request.method == 'POST':
        formset = WorkEventFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            count = 0
            for instance in instances:
                instance.member_organization = member_organization
                instance.save()
                count += 1
            form = WorkEventFormSet(queryset=Distro.objects.none())
            return render(
                request,
                "distribution/hours_create.html",
                {
                    "formset": form,
                    "range": range(50),
                    "message": str(count) + " Items Saved To the Database",
                    "helper": WorkEventFormHelper()
                }
            )
        else:
            return render(
                request,
                "distribution/hours_create.html",
                {
                    "formset": formset,
                    "range": range(50),
                    "helper": WorkEventFormHelper(),
                    "error": "Valid dates required for filled out lines."
                }
            )

    else:
        form = WorkEventFormSet
        queryset = WorkEvent.objects.none()
        GET = request.GET

        if "date_from" in GET or "date_until" in GET:
            form = EditWorkEventFormSet
            queryset = WorkEvent.objects.all()
            has_from = False
            has_until = False
            if not request.user.has_perm("distro.uniauth"):
                queryset = queryset.filter(
                    member_organization=member_organization)
                date_from = datetime.datetime.strptime(
                    GET.get("date_from"),
                    "%m/%d/%Y").date()
                has_from = True
                date_until = datetime.datetime.strptime(
                    GET.get("date_until"),
                    "%m/%d/%Y").date()
                has_until = True
            if has_from and has_until:
                queryset = queryset.filter(
                    date__gte=date_from,
                    date__lte=date_until)
            elif has_from:
                queryset = queryset.filter(date__gte=date_from)
            elif has_until:
                queryset = queryset.filter(date__lte=date_until)

        if GET.get("filter") != "Download":
            form = form(queryset=queryset)
            return render(
                request,

                'distribution/hours_create.html',
                {
                    'formset': form,
                    'range': range(50),
                    "helper": WorkEventFormHelper()
                }
            )

        else:
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = '{0}; filename="{1}"'.format(
                "attachment",
                "volunteer_hours.csv",
                )

            # Create the CSV writer using the HttpResponse as the "file."
            writer = csv.writer(response)
            writer.writerow([
                "first_name",
                "last_name",
                "date",
                "time",
                "group",
                "members",
                "task",
                "miles",
                "notes"
            ])

            for event in queryset:
                writer.writerow([
                    event.first_name,
                    event.last_name,
                    event.date,
                    event.time,
                    event.group,
                    event.members,
                    event.task,
                    event.miles,
                    event.notes
                    ])

            return response

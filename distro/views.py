# Create your views here.
import time
import datetime
import csv

import django.forms
from django.forms.widgets import TextInput
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms

from django.contrib.auth.decorators import permission_required

from django.forms.models import modelformset_factory

from farms.models import Farm
from distro.models import Distro
from recipientsite.models import RecipientSite


@permission_required('distro.auth')
def index(request):
    date_from = request.GET.get('date_from', '')
    date_until = request.GET.get('date_until', '')
    profle = request.user.profile_set.get()
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


@permission_required('distro.auth')
def entry(request):
    DistroFormSet = modelformset_factory(Distro, extra=int(10))
    member_organization = request.user.profile_set.get(
    ).member_organization
    if request.method == 'POST':
        formset = DistroFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
        #   pass
        #else:
    #       return HttpResponse(formset.errors)
            count = 0
            for instance in instances:
                instance.member_organization = request.user.profile_set.get(
                ).member_organization
                instance.save()
                count += 1
            form = DistroFormSet(queryset=Distro.objects.none())
            return render(
                request,
                'distribution/entry.html',
                {
                    'formset': form,
                    'range': range(50),
                    'message': str(count) + ' Items Saved To the Database'
                }
            )
        else:
            return render(
                request,
                "distribution/entry.html",
                {
                    "formset": formset,
                    "range": range(50),
                    "error": "Form Error. Empty rows must be completely blank."
                }
            )

    else:
        form = DistroFormSet(queryset=Distro.objects.none())
        if not request.user.has_perm('distro.uniauth'):
            for fo in form.forms:
                fo.fields['farm'].queryset = Farm.objects.filter(
                    member_organization=member_organization)
                fo.fields['recipient'].queryset = RecipientSite.objects.filter(
                    member_organization=member_organization)
        debug = dir(form)
        return render(
            request,
            'distribution/entry.html',
            {'formset': form, 'range': range(50), 'debug': debug}
        )


@permission_required('distro.auth')
def edit(request):
    date_from = request.GET.get('date_from', '')
    date_until = request.GET.get('date_until', '')
    mo = request.user.profile_set.get().member_organization
    if date_from:
        date_from = "{0}-{1}-{2}".format(
            date_from[6:],
            date_from[:2],
            date_from[3:5],
        )
    else:
        date_from = '2013-01-01'
    if date_until:
        date_until = "{0}-{1}-{2}".format(
            date_until[6:],
            date_until[:2],
            date_until[3:5],
        )
    else:
        date_until = '3013-01-01'
    DistroFormSet = modelformset_factory(Distro, extra=0, can_delete=True)
    if request.method == 'POST':
        formset = DistroFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save()
            queryset = Distro.objects.all()
            if not request.user.has_perm('distro.uniauth'):
                queryset = queryset.filter(member_organization=mo)
            form = DistroFormSet(queryset=queryset)
            return render(
                request,
                'distribution/edit.html',
                {'form': form})
    else:
        queryset = Distro.objects.filter(
            date__gte=date_from,
            date__lte=date_until
        )
        if not request.user.has_perm('distro.uniauth'):
            queryset = queryset.filter(
                date__gte=date_from,
                date__lte=date_until,
                member_organization=mo
            )
        form = DistroFormSet(queryset=queryset.order_by('-date_d'))
        return render(request, 'distribution/edit.html', {'formset': form})


@permission_required('distro.auth')
def download(request):
    mo = request.user.profile_set.get().member_organization
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=distribution.csv'

    # Create the CSV writer using the HttpResponse as the "file."
    writer = csv.writer(response)
    writer.writerow([
        'Distribution Date',
        'Recipient
        Site',
        'Crops',
        'Pounds',
        'Containers',
        'Farm',
        'Other (notes)',
        'Harvest Date',
        'Farm Delivery/Field Glean/Farmers Market',
        'Pickup/DropOff'
    ])

    if request.user.has_perm('distro.uniauth'):
        group = Distro.objects.all()
    else:
        group = Distro.objects.filter(member_organization=mo)
    for line in group:
        writer.writerow([
            line.date_d,
            line.recipient,
            line.crops,
            line.pounds,
            line.containers,
            line.farm,
            line.other,
            line.date,
            line.field_or_farm,
            line.del_or_pick,
        ])

    return response

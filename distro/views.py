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
from distro.models import Distro, WorkEvent
from distro.forms import WorkEventFormHelper, WorkEventFormSet
from generic.views import DateFilterMixin
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


@permission_required('distro.auth')
def entry(request):
    DistroFormSet = modelformset_factory(Distro, extra=int(10))
    member_organization = request.user.profile.member_organization
    sites = RecipientSite.objects.filter(
        member_organization=member_organization)
    if request.method == 'POST':
        formset = DistroFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
        #   pass
        #else:
    #       return HttpResponse(formset.errors)
            count = 0
            for instance in instances:

                instance.member_organization = member_organization
                instance.save()
                count += 1
            form = DistroFormSet(queryset=Distro.objects.none())
            return render(
                request,
                "distribution/entry.html",
                {
                    "formset": form,
                    "range": range(50),
                    "message": str(count) + " Items Saved To the Database",
                    "sites": sites,
                }
            )
        else:
            return render(
                request,
                "distribution/entry.html",
                {
                    "formset": formset,
                    "range": range(50),
                    "sites": sites,
                    "error": "Form Error. Empty rows must be completely blank."
                }
            )

    else:
        form = DistroFormSet(queryset=Distro.objects.none())
        if not request.user.has_perm('distro.uniauth'):
            for fo in form.forms:
                fo.fields['farm'].queryset = Farm.objects.filter(
                    member_organization=member_organization)
                #fo.fields['recipient'] = TextInput
        debug = dir(form)
        return render(
            request,

            'distribution/entry.html',
            {
                'formset': form,
                'range': range(50),
                'sites': sites,
                'debug': debug,
            }
        )


@permission_required('distro.auth')
def edit(request):
    date_from = request.GET.get('date_from', '')
    date_until = request.GET.get('date_until', '')
    mo = request.user.profile.member_organization
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


class WorkEventsListView(generic.ListView):
    model = WorkEvent
    template_name = "distribution/workevent_list.html"

    def get_queryset(self):
        user = self.request.user
        queryset = WorkEvent.objects.all()
        if not user.has_perm("workevent.uniauth"):
            memorg = user.profile.member_organization
            return queryset.filter(member_organization=memorg)

        try:
            from_d = datetime.date.strptime(
                self.request.GET["date_until"],
                "%m/%d/%Y")
            until_date = datetime.date.strptime(
                self.request.GET["date_until"],
                "%m/%d/%Y")
            queryset = queryset.filter(
                timestamp__gte=from_d,
                timestamp__lte=until_d
            )
        except:
            pass

        return queryset.filter


class WorkEventsCreateView(DateFilterMixin, generic.CreateView):
    model = WorkEvent
    template_name = "distribution/hours_create.html"

    def get_context_data(self, **kwargs):
        context = super(WorkEventsCreateView, self).get_context_data(**kwargs)
        context["workevent_form"] = WorkEventFormSet()
        if self.request.POST:
            #import pdb; pdb.set_trace()
            #WorkEventFormSet = modelformset_factory(WorkEvent)
            context["workevent_form"] = WorkEventFormSet(self.request.POST)
        else:
            if self.from_date or self.until_date:
                queryset = self.get_queryset()
                context["workevent_form"] = WorkEventFormSet(queryset=queryset)
        context["helper"] = WorkEventFormHelper()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        workevent_form = context["workevent_form"]
        if workevent_form.is_valid():
            self.object = workevent_form.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        if self.from_date and self.until_date:
            return WorkEvent.objects.filter(
                date__gte=self.from_date,
                date__lte=self.until_date
            )
        elif self.from_date:
            return WorkEvent.objects.filter(
                date__gte=self.from_date
            )
        elif self.from_date:
            return WorkEvent.objects.filter(
                date__lte=self.until_date
            )

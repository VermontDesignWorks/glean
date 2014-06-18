import sys
from django import forms
from counties.models import County
from django.forms import ModelForm
from crispy_forms.bootstrap import (FieldWithButtons,
                                    InlineCheckboxes,
                                    StrictButton,
                                    AppendedText)
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout,
                                 Fieldset,
                                 ButtonHolder,
                                 Field,
                                 Row,
                                 Submit,
                                 Div,
                                 HTML)

from constants import STATES, COLORS, LINE_TYPE
from farms.models import Farm
from counties.models import County
from memberorgs.models import MemOrg
from farms.models import FarmLocation


class Counties_For_Forms(ModelForm):
    'A class for easily including counties in a crispyform'

    version = '0.1'
    
    # properties of the class inherited into crispyform
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )
    vt_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False,
    )
    
    # initialize the class form with previous county information  (only use on edit forms not create forms)
    # object_toinit = kwargs['instance'] pass this in
    def county_initialize(self, object_toinit):

        self.initial["vt_counties"] = [
            x.pk for x in object_toinit.counties.filter(state="VT")
        ]
        self.initial["ny_counties"] = [
            x.pk for x in object_toinit.counties.filter(state="NY")
        ]

    # referred to with self.county_fieldset to be used when you require county fieldset
    @property
    def county_fieldset(self):
        return Fieldset(
            "",
            HTML("<h3 class='lbl'>Counties Operating"
                 " in</h3>"),
            Div(InlineCheckboxes("vt_counties"),
                InlineCheckboxes("ny_counties"),
                css_class="form-checkboxes")
        )

    # override to save form to save counties and such
    def save(self, *args, **kwargs):
        saved = super(Counties_For_Forms, self).save(*args, **kwargs)
        if 'vt_counties' in self.data:
            for pk in self.data.getlist('vt_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
        if 'ny_counties' in self.data:
            for pk in self.data.getlist('ny_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
        saved.save()
        return saved

    class Meta:
        model = County


class FarmLocBase(ModelForm):

    name = forms.CharField(max_length=200)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 460px'}),
        required=False)
    address_one = forms.CharField(label='Address:', max_length=200)
    address_two = forms.CharField(
        label='Address (line two):',
        max_length=200,
        required=False)
    city = forms.CharField(label='City:', max_length=200)
    state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    zipcode = forms.CharField(label='Zip Code:', max_length=11)

    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address', required=False)
    mailing_address_one = forms.CharField(
        label='Address: ', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Address (line two):', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='City:', max_length=200, required=False)
    mailing_state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    mailing_zip = forms.CharField(
        label='Zip Code:', max_length=11, required=False)
    directions = forms.CharField(
        label='Directions:',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 460px'}),
        required=False)
    instructions = forms.CharField(
        label='Instructions:',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 460px'}),
        required=False)
    ny_counties_single = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )
    vt_counties_single = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False
    )
    county_fieldset = Fieldset(HTML("<h3 class='lbl'>County of Operation"
                               " <small>(select One)</small></h3>"),
                               Div(InlineCheckboxes("vt_counties_single"),
                               InlineCheckboxes("ny_counties_single"),
                               css_class="form-checkboxes",
                               style="width: 460px;"))

    def county_initialize(self, object_toinit):
        self.initial["vt_counties_single"] = [object_toinit.counties]
        self.initial["ny_counties_single"] = [object_toinit.counties]

    def save(self, *args, **kwargs):
        saved = super(FarmLocBase, self).save(*args, **kwargs)
        if 'vt_counties_single' in self.data:
            for pk in self.data.getlist('vt_counties_single'):
                county = County.objects.get(pk=pk)
                saved.counties = county
        if 'ny_counties_single' in self.data:
            for pk in self.data.getlist('ny_counties_single'):
                county = County.objects.get(pk=pk)
                saved.counties = county
        saved.save()
        return saved
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
    'A class for Multiple county select accross the site'

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


class County_For_Forms(ModelForm):
    'For Single County Select form section accross the site'

    version = '0.1'

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
        saved = super(County_For_Forms, self).save(*args, **kwargs)
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
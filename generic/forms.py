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
        return saved

    class Meta:
        model = County
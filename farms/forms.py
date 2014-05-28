from django import forms
from django.forms import ModelForm
from django.forms.fields import ChoiceField
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


class FarmForm(ModelForm):
    class Meta:
        model = Farm
        exclude = ['farmers']


class NewFarm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewFarm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-New-Farm-Form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div style='float: right; display: inline; border-left: 10px solid #ffc64a;'>"),
            HTML("<i style='color: red;'>Information in this column is visable only by administrators</i>"),
            Fieldset(
                "",
                HTML("<h3>Mailing Address</h3"),
                Row("physical_is_mailing"),
                Row("mailing_address_one", "mailing_address_two"),
                Row("mailing_city", "mailing_state"),
                Row("mailing_zip"),
                Row("description"),
                Row("phone_1", "phone_1_type"),
                Row("Phone_2", "phone_2_type"),
                Row("email"),
            ),
            HTML("</div>"),
            HTML("<div>"),
            HTML("<div style='float:left; display: inline;'>"),
            Fieldset(
                "",
                Row("name"),
                HTML("<h3>Physical Address</h3>"),
                Row("address_one, address_two"),
                Row("city", "state"),
                Row("zipcode"),
                Row("directions"),
                Row("instructions"),
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>Counties Operating"
                     " in</h3>"),
                Div(InlineCheckboxes("vt_counties"),
                    InlineCheckboxes("ny_counties"),
                    css_class="form-checkboxes")
            ),
            HTML("</div>"),
            HTML("</div>"),
            HTML("<div style='display: inline-block;'>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Add Farm'>"),
            HTML("</div>")
        )

    name = forms.CharField(max_length=200)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
    address_one = forms.CharField(label='Address:', max_length=200)
    address_two = forms.CharField(label='Address (line two):', max_length=200)
    city = forms.CharField(label='City:', max_length=200)
    state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    zipcode = forms.CharField(label='Zip Code:', max_length=11)
    
    physical_is_mailing = forms.BooleanField(label='Physical Address is Mailing Address')
    mailing_address_one = forms.CharField(label='Address: ', max_length=200)
    mailing_address_two = forms.CharField(label='Address (line two):', max_length=200)
    mailing_city = forms.CharField(label='City:', max_length=200)
    mailing_state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    mailing_zip = forms.CharField(label='Zip Code:', max_length=11)

    phone_1 = forms.CharField(label='Primary phone #:', max_length=200)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(label='Secondary phone #:', max_length=200)
    phone_2_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    email = forms.CharField(label="Email:")
    directions = forms.CharField(
        label='Directions:',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
    instructions = forms.CharField(
        label='Instructions:',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
    vt_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False,
    )
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )

    class Meta:
        model = Farm
        exclude = ("farmers","member_organization")
import sys
from django import forms
from django.forms import ModelForm
from django.forms.fields import ChoiceField
from crispy_forms.bootstrap import (FieldWithButtons,
                                    InlineCheckboxes,
                                    InlineRadios,
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
from farms.models import Farm, FarmLocation
from counties.models import County
from memberorgs.models import MemOrg
from recipientsite.models import RecipientSite


class RecipientSiteForm(ModelForm):
    'A crispyform class for creating a new recipient site object'

    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(RecipientSiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-New-Farm-Form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Row("name"),
                    Row("address_one", "address_two"),
                    Row("city", "state"),
                    Row("zipcode"),
                    "description",
                    css_class="crispy_column_left"),
                Div(
                    HTML("<p class='red-emphasized'>Information in this"
                         " column is visible only by administrators</p>"),
                    "physical_is_mailing",
                    Row("mailing_address_one", "mailing_address_two"),
                    Row("mailing_city", "mailing_state"),
                    "mailing_zip",
                    Row("primary_contact"),
                    Row("phone", "email"),
                    css_class="crispy_column_left yellow-left")
            ),
            HTML("</div>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Recipient Site'>"),
            HTML("</div>")
        )

    name = forms.CharField(label="Name")
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 460px'}),
        required=False)
    address_one = forms.CharField(max_length=20, required=False)
    address_two = forms.CharField(max_length=20, required=False)
    city = forms.CharField(max_length=20, required=False)
    state = forms.ChoiceField(choices=STATES, required=False)
    zipcode = forms.CharField(max_length=10, required=False)
    member_organization = forms.ModelMultipleChoiceField(
        queryset=MemOrg.objects.all(), required=False)

    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address', required=False)
    mailing_address_one = forms.CharField(
        label='Mailing Address (line one)', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Mailing Address (line two)', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='Mailing Address (City)', max_length=200, required=False)
    mailing_state = forms.ChoiceField(
        label='Mailing Address (State)', choices=STATES, required=False)
    mailing_zip = forms.CharField(
        label='Mailing Address Zipcode', max_length=11, required=False)

    primary_contact = forms.CharField(
        label='Primary Contact First Name', max_length=30, required=False)
    phone = forms.CharField(
        label='Primary Phone', max_length=20, required=False)
    email = forms.CharField(
        label='Email', max_length=40, required=False)
    
    class Meta:
        model = RecipientSite
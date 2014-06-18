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
from generic.forms import FarmLocBase


class NewFarmForm(FarmLocBase, ModelForm):
    'A crispyform class for creating a new farm object'

    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(NewFarmForm, self).__init__(*args, **kwargs)
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
                    "directions",
                    "instructions",
                    self.county_fieldset,
                    css_class="crispy_column_left"),
                Div(
                    HTML("<p class='red-emphasized'>Information in this"
                         " column is visible only by administrators</p>"),
                    "physical_is_mailing",
                    Row("mailing_address_one", "mailing_address_two"),
                    Row("mailing_city", "mailing_state"),
                    "mailing_zip",
                    "description",
                    Row("phone_1", "phone_1_type"),
                    Row("phone_2", "phone_2_type"),
                    "email",
                    css_class="crispy_column_left yellow-left")
            ),
            HTML("</div>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Add Farm'> <input type='submit'"
                 "class='glean-button red-button' "
                 "name='submit' value='Add Farm and Add Contact'>"),
            HTML("</div>")
        )

    phone_1 = forms.CharField(
        label='Primary phone #:',
        max_length=200,
        required=False)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(
        label='Secondary phone #:', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    email = forms.CharField(label="Email:", required=False)
    member_organization = forms.ModelMultipleChoiceField(
        label="member_organization",
        queryset=MemOrg.objects.all(),
        required=False)

    class Meta:
        model = Farm
        exclude = ("farmers",)


class EditFarmForm(FarmLocBase, ModelForm):
    'A crispyform class for editing a farm object'

    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(EditFarmForm, self).__init__(*args, **kwargs)
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
                    "directions",
                    "instructions",
                    self.county_fieldset,
                    css_class="crispy_column_left"),
                Div(
                    HTML("<p class='red-emphasized'>Information in this"
                         " column is visible only by administrators</p>"),
                    "physical_is_mailing",
                    Row("mailing_address_one", "mailing_address_two"),
                    Row("mailing_city", "mailing_state"),
                    "mailing_zip",
                    "description",
                    Row("phone_1", "phone_1_type"),
                    Row("phone_2", "phone_2_type"),
                    "email",
                    css_class="crispy_column_left yellow-left")
            ),
            HTML("</div>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'> <input type='submit'"
                 "class='glean-button red-button' "
                 "name='submit' value='Save Farm and Add Contact'>"),
            HTML("</div>")
        )
        farm = self.instance
        self.county_initialize(farm)

    phone_1 = forms.CharField(
        label='Primary phone #:',
        max_length=200,
        required=False)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(
        label='Secondary phone #:',
        max_length=200,
        required=False)
    phone_2_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    email = forms.CharField(label="Email:", required=False)
    member_organization = forms.ModelMultipleChoiceField(
        label="member_organization",
        queryset=MemOrg.objects.all(),
        required=False)

    class Meta:
        model = Farm
        exclude = ("farmers", "member_organization")


class NewLocationForm(FarmLocBase, ModelForm):
    'A crispyform class for editing a location object'

    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(NewLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-Edit-Location-Form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Row("name"),
                    Row("address_one", "address_two"),
                    Row("city", "state"),
                    Row("zipcode"),
                    "directions",
                    "instructions",
                    self.county_fieldset,
                    css_class="crispy_column_left"),
                Div(
                    HTML("<p class='red-emphasized'>Information in this"
                         " column is visible only by administrators</p>"),
                    "physical_is_mailing",
                    Row("mailing_address_one", "mailing_address_two"),
                    Row("mailing_city", "mailing_state"),
                    "mailing_zip",
                    "description",
                    css_class="crispy_column_left yellow-left")),
            HTML("</div>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Add Location'><input type='submit' "
                 "class='glean-button red-button' "
                 "name='submit' value='Add Location and Create Another'>"),
            HTML("</div>"))

    class Meta:
        model = FarmLocation


class EditLocationForm(FarmLocBase, ModelForm):
    'A crispyform class for editing a location object'

    version = '0.1'

    def __init__(self, *args, **kwargs):
        super(EditLocationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-Edit-Location-Form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Div(
                    Row("name"),
                    Row("address_one", "address_two"),
                    Row("city", "state"),
                    Row("zipcode"),
                    "directions",
                    "instructions",
                    self.county_fieldset,
                    css_class="crispy_column_left"),
                Div(
                    HTML("<p class='red-emphasized'>Information in this"
                         " column is visible only by administrators</p>"),
                    "physical_is_mailing",
                    Row("mailing_address_one", "mailing_address_two"),
                    Row("mailing_city", "mailing_state"),
                    "mailing_zip",
                    "description",
                    css_class="crispy_column_left yellow-left")),
            HTML("</div>"),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'><input type='submit' "
                 "class='glean-button red-button' "
                 "name='submit' value='Save and Create Another'>"),
            HTML("</div>"))
        location = self.instance
        self.county_initialize(location)

    class Meta:
        model = FarmLocation

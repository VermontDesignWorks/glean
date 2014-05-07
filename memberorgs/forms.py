from django import forms

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

from counties.models import County
from memberorgs.models import MemOrg
from userprofile.models import Profile
from constants import STATES, COLORS, LINE_TYPE


class AdminMemOrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-memorgs-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("name", "website"),
                Row("description"),
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>Counties member organization will manage</h3>"),
                Div(InlineCheckboxes("vt_counties"),
                    InlineCheckboxes("ny_counties"),
                    css_class="form-checkboxes")
            ),
            Fieldset(
                "",
                Row("volunteers", "color"),
                Row("address_one"),
                Row("address_two"),
                Row("city", "state"),
                Row("zipcode"),
                Row("physical_is_mailing"),
                Row("mailing_address_one"),
                Row("mailing_address_two"),
                Row("mailing_city", "mailing_state"),
                Row("mailing_zip"),
            )
            )
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50)
    description = forms.CharField(label='Description', widget=forms.Textarea)
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
    volunteers = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Profile.objects,
        label="Volunteers",
        required=False)

    color = forms.ChoiceField(
        label="Colors", choices=COLORS)

    address_one = forms.CharField(
        label='Physical Address (line one)', max_length=30)
    address_two = forms.CharField(
        label='Physical Address (line two)', max_length=30)
    city = forms.CharField(label='City', max_length=15)
    state = forms.ChoiceField(
        label="State", choices=STATES)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11)
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address')

    mailing_address_one = forms.CharField(
        label='Mailing Address (line one)', max_length=200)
    mailing_address_two = forms.CharField(
        label='Mailing Address (line two)', max_length=200)
    mailing_city = forms.CharField(
        label='Mailing Address (City)', max_length=200)
    mailing_state = forms.ChoiceField(label='State', choices=STATES)
    mailing_zip = forms.CharField(
        label='Mailing Address Zipcode', max_length=11)

    phone_1 = forms.CharField(
        label='Primary phone', max_length=200)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE)
    phone_2 = forms.CharField(
        label='Secondary phone', max_length=200)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE)

    first_name = forms.CharField(
        label="Executive Director First Name", max_length=20)
    last_name = forms.CharField(
        label="Executive Director Last Name", max_length=20)
    phone = forms.CharField(
        label="Director's Direct Phone Number", max_length=15)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?')

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address")

    testing_email = forms.CharField(
        label="Primary Email Address", max_length="200")
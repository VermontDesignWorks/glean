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
    volunteers = forms.ManyToManyField(
        User, editable=False, related_name="member_organizations")

    color = forms.CharField(
        'Color', choices=COLORS, max_length=20, default='muted')

    address_one = forms.CharField(
        'Physical Address (line one)', max_length=30, blank=True, null=True)
    address_two = forms.CharField(
        'Physical Address (line two)', max_length=30, blank=True, null=True)
    city = forms.CharField('City', max_length=15, blank=True, null=True)
    state = forms.CharField(
        "State", choices=STATES, default="VT", max_length=2, blank=True)
    zipcode = forms.CharField(
        "Zipcode", max_length=11, blank=True, null=True)
    physical_is_mailing = forms.BooleanField(
        'Physical Address is Mailing Address', default=True)

    mailing_address_one = forms.CharField(
        'Mailing Address (line one)', max_length=200, blank=True)
    mailing_address_two = forms.CharField(
        'Mailing Address (line two)', max_length=200, blank=True)
    mailing_city = forms.CharField(
        'Mailing Address (City)', max_length=200, blank=True)
    mailing_state = forms.CharField(
        'Mailing Address (State)', choices=STATES, max_length=2, blank=True)
    mailing_zip = forms.CharField(
        'Mailing Address Zipcode', max_length=11, blank=True)

    phone_1 = forms.CharField(
        'Primary phone', max_length=200, blank=True)
    phone_1_type = forms.CharField(
        'Primary Phone Type', choices=LINE_TYPE, max_length=10, blank=True)
    phone_2 = forms.CharField(
        'Secondary phone', max_length=200, blank=True)
    phone_2_type = forms.CharField(
        'Secondary Phone Type', choices=LINE_TYPE, max_length=10, blank=True)

    first_name = forms.CharField(
        "Executive Director First Name", max_length=20, blank=True)
    last_name = forms.CharField(
        "Executive Director Last Name", max_length=20, blank=True)
    phone = forms.CharField(
        "Director's Direct Phone Number", max_length=15, blank=True, null=True)

    notify = forms.BooleanField(
        'Notify on New Volunteer Signup?', default=False)

    testing = forms.BooleanField(
        "Relay Announcement Emails to Testing Address", default=True)

    testing_email = forms.CharField(
        "Primary Email Address", max_length="200", blank=True)
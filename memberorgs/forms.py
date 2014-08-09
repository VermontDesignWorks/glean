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

from django.contrib.auth.models import User

from counties.models import County
from memberorgs.models import MemOrg
from userprofile.models import Profile
from constants import STATES, COLORS, LINE_TYPE

from django.db.models import Q

from generic.forms import Counties_For_Forms


class UserMultipleModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        profile = obj.profile
        return "%s %s" % (profile.first_name, profile.last_name)


class AdminMemOrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminMemOrgForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-memorgs-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("name", "website"),
                Row("description"),
                Row("phone_1", "phone_1_type"),
                Row("phone_2", "phone_2_type"),
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>Counties member"
                     " organization will manage</h3>"),
                Div(InlineCheckboxes("vt_counties"),
                    InlineCheckboxes("ny_counties"),
                    css_class="form-checkboxes")
            ),
            Fieldset(
                "",
                HTML("<h3>Physical Address</h3>"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode"),
                HTML("<h3>Mailing Address</h3>"),
                Row("physical_is_mailing"),
                Row("mailing_address_one", "mailing_address_two"),
                Row("mailing_city", "mailing_state"),
                Row("mailing_zip"),
                HTML("<h3>Executive Director Information</h3>"),
                Row("first_name", "last_name"),
                Row("phone")
            ),
            Fieldset(
                "",
                HTML("<h3>Administrative Email Updates</h3>"),
                Row("testing"),
                HTML("<h4>All test emails will go to"
                     " the address specificed below:</h4>"),
                Row("testing_email"),
                HTML("<h4>&nbsp;</h4>"),
                Row("notify"),
                HTML("<h4>All notification emails will go to"
                     " the address specificed below:</h4>"),
                Row("notification_email")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
        )
        memorg = kwargs["instance"]
        self.initial["vt_counties"] = [
            x.pk for x in memorg.counties.filter(state="VT")
        ]
        self.initial["ny_counties"] = [
            x.pk for x in memorg.counties.filter(state="NY")
        ]
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50, required=False)
    description = forms.CharField(
        label='Description',
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
    color = forms.ChoiceField(
        label="Colors", choices=COLORS, required=False)
    address_one = forms.CharField(
        label='Address', max_length=30, required=False)
    address_two = forms.CharField(
        label='Address (line two)', max_length=30, required=False)
    city = forms.CharField(label='City', max_length=15, required=False)
    state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11, required=False)
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address', required=False)
    mailing_address_one = forms.CharField(
        label='Address', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Address (line two)', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='City', max_length=200, required=False)
    mailing_state = forms.ChoiceField(label='State', choices=STATES,
                                      required=False)
    mailing_zip = forms.CharField(
        label='Mailing Address Zipcode', max_length=11, required=False)

    phone_1 = forms.CharField(
        label='Primary phone #', max_length=200, required=False)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(
        label='Secondary phone #', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE, required=False)

    first_name = forms.CharField(
        label="First Name", max_length=20, required=False)
    last_name = forms.CharField(
        label="Last Name", max_length=20, required=False)
    phone = forms.CharField(
        label="Phone #", max_length=15, required=False)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?', required=False)

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address", required=False)

    testing_email = forms.CharField(
        label="Member Organization Test (beta mode) Email Address",
        max_length="200",
        required=False)

    notification_email = forms.CharField(
        label="Member Organization New Member Notification Email Address",
        max_length="200",
        required=False)

    class Meta:
        model = MemOrg

    def save(self, *args, **kwargs):
        saved = super(AdminMemOrgForm, self).save(*args, **kwargs)
        if 'vt_counties' in self.data:
            for pk in self.data.getlist('vt_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
        if 'ny_counties' in self.data:
            for pk in self.data.getlist('ny_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
        return saved


class MemOrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemOrgForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-memorgs-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("name", "website"),
                Row("description"),
                Row("phone_1", "phone_1_type"),
                Row("phone_2", "phone_2_type"),
            ),
            Fieldset(
                "",
                HTML("<h3>Physical Address</h3>"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode"),
                HTML("<h3>Mailing Address</h3>"),
                Row("physical_is_mailing"),
                Row("mailing_address_one", "mailing_address_two"),
                Row("mailing_city", "mailing_state"),
                Row("mailing_zip"),
                HTML("<h3>Executive Director Information</h3>"),
                Row("first_name", "last_name"),
                Row("phone")
            ),
            Fieldset(
                "",
                Row("notify"),
                Row("testing"),
                Row("testing_email")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
        )
        memorg = kwargs["instance"]
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50, required=False)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)

    color = forms.ChoiceField(
        label="Colors", choices=COLORS, required=False)

    address_one = forms.CharField(
        label='Address', max_length=30, required=False)
    address_two = forms.CharField(
        label='Address (line two)', max_length=30, required=False)
    city = forms.CharField(label='City', max_length=15, required=False)
    state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11, required=False)
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address', required=False)

    mailing_address_one = forms.CharField(
        label='Address', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Address (line two)', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='City', max_length=200, required=False)
    mailing_state = forms.ChoiceField(label='State', choices=STATES,
                                      required=False)
    mailing_zip = forms.CharField(
        label='Zipcode', max_length=11, required=False)

    phone_1 = forms.CharField(
        label='Primary phone #', max_length=200, required=False)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(
        label='Secondary phone #', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE, required=False)

    first_name = forms.CharField(
        label="First Name", max_length=20, required=False)
    last_name = forms.CharField(
        label="Last Name", max_length=20, required=False)
    phone = forms.CharField(
        label="Phone #", max_length=15, required=False)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?', required=False)

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address", required=False)

    testing_email = forms.CharField(
        label="Testing Email Address", max_length="200", required=False)

    class Meta:
        model = MemOrg
        exclude = ("counties",)


class NewMemOrgForm(Counties_For_Forms, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewMemOrgForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-memorgs-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("name", "website"),
                Row("description"),
                Row("phone_1", "phone_1_type"),
                Row("phone_2", "phone_2_type"),
            ),
            self.county_fieldset,
            Fieldset(
                "",
                HTML("<h3>Physical Address</h3>"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode"),
                HTML("<h3>Mailing Address</h3>"),
                Row("physical_is_mailing"),
                Row("mailing_address_one", "mailing_address_two"),
                Row("mailing_city", "mailing_state"),
                Row("mailing_zip"),
                HTML("<h3>Executive Director Information</h3>"),
                Row("first_name", "last_name"),
                Row("phone")
            ),
            Fieldset(
                "",
                Row("notify"),
                Row("notification_email")
                Row("testing"),
                Row("testing_email")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
        )
        memorg = kwargs["instance"]
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50, required=False)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
    color = forms.ChoiceField(
        label="Colors", choices=COLORS, required=False)
    address_one = forms.CharField(
        label='Address', max_length=30, required=False)
    address_two = forms.CharField(
        label='Address (line two)', max_length=30, required=False)
    city = forms.CharField(label='City', max_length=15, required=False)
    state = forms.ChoiceField(
        label="State", choices=STATES, required=False)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11, required=False)
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address', required=False)
    mailing_address_one = forms.CharField(
        label='Address', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Address (line two)', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='City', max_length=200, required=False)
    mailing_state = forms.ChoiceField(label='State', choices=STATES,
                                      required=False)
    mailing_zip = forms.CharField(
        label='Mailing Address Zipcode', max_length=11, required=False)

    phone_1 = forms.CharField(
        label='Primary phone #', max_length=200, required=False)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE, required=False)
    phone_2 = forms.CharField(
        label='Secondary phone #', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE, required=False)

    first_name = forms.CharField(
        label="First Name", max_length=20, required=False)
    last_name = forms.CharField(
        label="Last Name", max_length=20, required=False)
    phone = forms.CharField(
        label="Phone #", max_length=15, required=False)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?', required=False)

    notification_email = forms.CharField(
        label="Notification Email Address", max_length="200", required=False)

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address", required=False)

    testing_email = forms.CharField(
        label="Testing Email Address", max_length="200", required=False)

    class Meta:
        model = MemOrg

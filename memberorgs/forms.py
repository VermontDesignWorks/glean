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

<<<<<<< HEAD
from django.contrib.auth.models import User
=======
>>>>>>> master
from counties.models import County
from memberorgs.models import MemOrg
from userprofile.models import Profile
from constants import STATES, COLORS, LINE_TYPE

<<<<<<< HEAD
from django.db.models import Q


class UserMultipleModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        profile = obj.profile
        return "%s %s" % (profile.first_name, profile.last_name)


class AdminMemOrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminMemOrgForm, self).__init__(*args, **kwargs)
=======

class AdminMemOrgForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
>>>>>>> master
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-memorgs-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("name", "website"),
                Row("description"),
<<<<<<< HEAD
                Row("phone_1", "phone_1_type"),
                Row("phone_2", "phone_2_type"),
=======
>>>>>>> master
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
<<<<<<< HEAD
                Row("volunteers"),
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
        self.initial["vt_counties"] = [
            x.pk for x in memorg.counties.filter(state="VT")
        ]
        self.initial["ny_counties"] = [
            x.pk for x in memorg.counties.filter(state="NY")
        ]
        self.initial["volunteers"] = [
            x.pk for x in memorg.volunteers.order_by(
                "last_name").order_by("first_name")
        ]
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50, required=False)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
=======
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
>>>>>>> master
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
<<<<<<< HEAD
    volunteers = UserMultipleModelChoiceField(
        queryset=User.objects.order_by("last_name").order_by("first_name"),
=======
    volunteers = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=Profile.objects,
>>>>>>> master
        label="Volunteers",
        required=False)

    color = forms.ChoiceField(
<<<<<<< HEAD
        label="Colors", choices=COLORS, required=False)

    address_one = forms.CharField(
        label='Address', max_length=30)
    address_two = forms.CharField(
        label='ddress (line two)', max_length=30, required=False)
=======
        label="Colors", choices=COLORS)

    address_one = forms.CharField(
        label='Physical Address (line one)', max_length=30)
    address_two = forms.CharField(
        label='Physical Address (line two)', max_length=30)
>>>>>>> master
    city = forms.CharField(label='City', max_length=15)
    state = forms.ChoiceField(
        label="State", choices=STATES)
    zipcode = forms.CharField(
<<<<<<< HEAD
        label="Zipcode", max_length=11, required=False)
=======
        label="Zipcode", max_length=11)
>>>>>>> master
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address')

    mailing_address_one = forms.CharField(
<<<<<<< HEAD
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
        label='Primary phone #', max_length=200)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE)
    phone_2 = forms.CharField(
        label='Secondary phone #', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE, required=False)

    first_name = forms.CharField(
        label="First Name", max_length=20)
    last_name = forms.CharField(
        label="Last Name", max_length=20)
    phone = forms.CharField(
        label="Phone #", max_length=15)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?', required=False)

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address", required=False)

    testing_email = forms.CharField(
        label="Testing Email Address", max_length="200", required=False)

    class Meta:
        model = MemOrg


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
                Row("volunteers"),
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
        self.initial["volunteers"] = [
            x.pk for x in memorg.volunteers.order_by("last_name").order_by("first_name")
        ]
    name = forms.CharField(label='name', max_length=200)
    website = forms.CharField(label='Website', max_length=50, required=False)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'cols': '100', 'rows': '10', 'style': 'width: 450px'}),
        required=False)
    volunteers = UserMultipleModelChoiceField(
        queryset=User.objects.order_by("last_name").order_by("first_name"),
        label="Volunteers",
        required=False)

    color = forms.ChoiceField(
        label="Colors", choices=COLORS, required=False)

    address_one = forms.CharField(
        label='Address', max_length=30)
    address_two = forms.CharField(
        label='Address (line two)', max_length=30, required=False)
    city = forms.CharField(label='City', max_length=15)
    state = forms.ChoiceField(
        label="State", choices=STATES)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11, required=False)
    physical_is_mailing = forms.BooleanField(
        label='Physical Address is Mailing Address')

    mailing_address_one = forms.CharField(
        label='Address (line one)', max_length=200, required=False)
    mailing_address_two = forms.CharField(
        label='Address (line two)', max_length=200, required=False)
    mailing_city = forms.CharField(
        label='City', max_length=200, required=False)
    mailing_state = forms.ChoiceField(label='State', choices=STATES,
                                      required=False)
    mailing_zip = forms.CharField(
        label='Zipcode', max_length=11, required=False)

    phone_1 = forms.CharField(
        label='Primary phone #', max_length=200)
    phone_1_type = forms.ChoiceField(
        label='Primary Phone Type', choices=LINE_TYPE)
    phone_2 = forms.CharField(
        label='Secondary phone #', max_length=200, required=False)
    phone_2_type = forms.ChoiceField(
        label='Secondary Phone Type', choices=LINE_TYPE, required=False)

    first_name = forms.CharField(
        label="First Name", max_length=20)
    last_name = forms.CharField(
        label="Last Name", max_length=20)
    phone = forms.CharField(
        label="Phone #", max_length=15)

    notify = forms.BooleanField(
        label='Notify on New Volunteer Signup?', required=False)

    testing = forms.BooleanField(
        label="Relay Announcement Emails to Testing Address", required=False)

    testing_email = forms.CharField(
        label="Testing Email Address", max_length="200", required=False)

    class Meta:
        model = MemOrg
        exclude = ("ny_counties","vt_counties")
=======
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
>>>>>>> master

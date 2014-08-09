from django import forms
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string

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
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm

from counties.models import County
from memberorgs.models import MemOrg
from userprofile.models import Profile

from constants import AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, STATES, TASKS


class ExtendedRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super(ExtendedRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                HTML("<h3 class='lbl'>Your Information</h3>"
                     "<h4>Please fill in all the below information"
                     " to create your account.</h4>"),
                Row("username", "email"),
                Row("password1", "password2"),
                Row("first_name", "last_name"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode", "age"),
                Row("phone", "phone_type"),
                Row("preferred_method")
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>Emergency Contact Information</h3>"),
                Row("ecfirst_name",
                    "eclast_name"),
                Row("ecphone",
                    "ecrelationship"),
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl' id='counties-box'>Counties"
                     " You'd Like to Glean In*</h3>"),
                HTML("<h4>Volunteers are notified of gleans based on the"
                     " counties they select,<br> if you don't select at least "
                     "one county you will not recieve<br>gleaning invitations."
                     "</h4>"),
                Div(InlineCheckboxes("vt_counties"),
                    InlineCheckboxes("ny_counties"),
                    css_class="form-checkboxes")
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>How would you like"
                     " to participate?</h3>"),
                "tasks_gleaning",
                "tasks_farm_pickups",
                "tasks_delivery",
                "tasks_admin",
                "tasks_processing",
                HTML("<h3 class='lbl'>Additional Information</h3>"),
                Field("notes", css_class="form-notes")
            ),
            Fieldset(
                "",
                HTML("<h3 class='lbl'>We want you to be safe and happy...</h3>"
                     "<h4>Please read and consider these agreements"
                     " before committing to be a gleaner.</h4>"
                     "<h5>If you are under 18, please have"
                     " a parent or guardian "
                     "review this form too when"
                     " you click the register button at "
                     "the bottom of this page,"
                     " you're indicating their acceptance "
                     "of the terms on your behalf.</h5>"),
                AppendedText('waiver', '<a href="#waiver-modal" role="button"'
                             ' data-toggle="modal"><button class="glean-button'
                             ' yellow-button no-margin">View Waiver'
                             '</button></a>'),
                AppendedText('agreement', '<a href="#agreement-modal" '
                             'role="button" data-toggle="modal"><button'
                             ' class="glean-button yellow-button no-margin">'
                             'View Volunteer Agreement</button></a>'),
                AppendedText('photo_release', '<a href="#photo-release" '
                             'role="button" data-toggle="modal"><button'
                             ' class="glean-button yellow-button no-margin">'
                             'View Photo Release</button></a>'),
                HTML("<h4>Keep me in the loop! Click to receive email "
                     "updates &amp; newsletters from Salvation Farms."
                     "</h4>"),
                "opt_in"
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Register'>")
        )

    first_name = forms.CharField(label="First Name", max_length=20)
    last_name = forms.CharField(label="Last Name", max_length=20)
    address_one = forms.CharField(label="Address", max_length=200)
    address_two = forms.CharField(
        label="Address (line two)", max_length=200, required=False)
    city = forms.CharField(label="City", max_length=200)
    state = forms.ChoiceField(
        label="State",
        choices=STATES,
        initial='VT')
    zipcode = forms.CharField(label="Zipcode", max_length=11, required=False)
    vt_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="VT").order_by("name"),
        label="Counties in Vermont",
        required=False
    )
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )
    age = forms.ChoiceField(label="Age",
                            choices=AGE_RANGES)
    phone = forms.CharField(label="Primary Phone", max_length=200)
    phone_type = forms.ChoiceField(
        label="Phone Type", choices=PHONE_TYPE, initial='1')
    preferred_method = forms.ChoiceField(
        label="How Should We Contact You?",
        choices=PREFERRED_CONTACT,
    )

    ecfirst_name = forms.CharField(
        label="First Name", max_length=200)
    eclast_name = forms.CharField(
        label="Last Name", max_length=200)
    ecphone = forms.CharField(label="Phone", max_length=200)
    ecrelationship = forms.CharField(label="Relationship", max_length=200)
    tasks = forms.ChoiceField(label="Which Volunteer Opportunities most "
                              "interest you?", choices=TASKS,
                              required=False)
    tasks_gleaning = forms.BooleanField(
        label="Field Gleaning",
        required=False,
        initial=False
    )
    tasks_farm_pickups = forms.BooleanField(
        label="Farmers Market/Farm Pick-ups",
        required=False
    )
    tasks_delivery = forms.BooleanField(
        label="Delivery/Distribution",
        required=False
    )
    tasks_admin = forms.BooleanField(
        label="Administrative Support",
        required=False
    )
    tasks_processing = forms.BooleanField(
        label="Processing",
        required=False
    )
    notes = forms.CharField(label="Is there anything we should be aware"
                            " of? <br />i.e. I have a pick-up truck, or "
                            "I would like to bring a "
                            "group out to glean.<br />Please be brief.",
                            widget=forms.Textarea,
                            required=False)
    waiver = forms.BooleanField(
        label="Do you accept the Waiver of Liability?", required=True)
    agreement = forms.BooleanField(
        label="Do you accept the Volunteer Agreement?", required=True)
    photo_release = forms.BooleanField(
        label="Do you accept the Photo Release?", required=False)
    opt_in = forms.BooleanField(label="", required=False)


class AdminExtendedRegistrationForm(RegistrationForm):
    first_name = forms.CharField(label="First Name", max_length=20)
    last_name = forms.CharField(label="Last Name", max_length=20)
    address_one = forms.CharField(
        label="Address", max_length=200, required=False)
    address_two = forms.CharField(
        label="Address (line two)", max_length=200, required=False)
    city = forms.CharField(label="City", max_length=200, required=False)
    state = forms.ChoiceField(
        label="State", choices=STATES, initial='VT', required=False)
    zipcode = forms.CharField(
        label="Zipcode", max_length=11, required=False)
    counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.all(),
        label="Counties",
        required=False)
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY"),
        label="Counties in New York",
        required=False
    )
    age = forms.ChoiceField(label="Age",
                            choices=AGE_RANGES, required=False)
    phone = forms.CharField(
        label="Primary Phone", max_length=200, required=False)
    phone_type = forms.ChoiceField(
        label="Phone Type", choices=PHONE_TYPE, initial='1', required=False)
    preferred_method = forms.ChoiceField(
        label="Primary Contact Method",
        choices=PREFERRED_CONTACT,
        required=False
    )

    ecfirst_name = forms.CharField(
        label="Emergency Contact First Name", max_length=200, required=False)
    eclast_name = forms.CharField(
        label="Emergency Contact Last Name", max_length=200, required=False)
    ecphone = forms.CharField(
        label="Emergency Contact Phone", max_length=200, required=False)
    ecrelationship = forms.CharField(
        label="Relationship", max_length=200, required=False)

    waiver = forms.BooleanField(label="Waiver of Liability?", required=True)
    agreement = forms.BooleanField(label="Volunteer Agreement", required=True)
    photo_release = forms.BooleanField(label="Photo Release?", required=False)
    opt_in = forms.BooleanField(label="Email Opt-In?", required=False)


class MyRegistrationView(RegistrationView):
    form_class = ExtendedRegistrationForm

    def get_success_url(self, request, user):
        messages.add_message(
            request,
            messages.SUCCESS,
            "Your Account Has been Created! Login Below:"
        )
        return reverse_lazy("auth_login")

    def register(self, request, **cleaned_data):
        user = super(MyRegistrationView, self).register(
            request,
            **cleaned_data
        )
        user.is_active = True
        user.save()
        profile = Profile.objects.create(
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            address_one=cleaned_data['address_one'],
            address_two=cleaned_data['address_two'],
            city=cleaned_data['city'],
            state=cleaned_data['state'],
            zipcode=cleaned_data['zipcode'],
            age=cleaned_data['age'],
            phone=cleaned_data['phone'],
            phone_type=cleaned_data['phone_type'],
            ecphone=cleaned_data['ecphone'],
            preferred_method=cleaned_data['preferred_method'],
            ecfirst_name=cleaned_data['ecfirst_name'],
            eclast_name=cleaned_data['eclast_name'],
            ecrelationship=cleaned_data['ecrelationship'],
            user=user,
            waiver=cleaned_data['waiver'],
            agreement=cleaned_data['agreement'],
            tasks_gleaning=cleaned_data['tasks_gleaning'],
            tasks_farm_pickups=cleaned_data['tasks_farm_pickups'],
            tasks_delivery=cleaned_data['tasks_delivery'],
            tasks_admin=cleaned_data['tasks_admin'],
            tasks_processing=cleaned_data['tasks_processing'],
            notes=cleaned_data['notes'],
            photo_release=cleaned_data['photo_release'],
            opt_in=cleaned_data['opt_in']
        )

        for county in cleaned_data['vt_counties']:
            profile.counties.add(county)
        for county in cleaned_data['ny_counties']:
            profile.counties.add(county)

        profile.notify_registration()

        return user

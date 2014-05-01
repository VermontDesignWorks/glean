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

from constants import AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, STATES, TASKS


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "",
                Row("first_name", "last_name"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode", "age"),
                Row("phone", "phone_type"),
                Row("email",  "preferred_method")
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
                HTML("<h3 class='lbl'>Counties You'd Like to Glean In</h3>"),
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
        profile = kwargs["instance"]
        self.initial["vt_counties"] = [
            x.pk for x in profile.counties.filter(state="VT")
        ]
        self.initial["ny_counties"] = [
            x.pk for x in profile.counties.filter(state="NY")
        ]
        self.initial["email"] = profile.user.email

    first_name = forms.CharField(label="First Name", max_length=20)
    email = forms.EmailField(label="Email", max_length=20, required=False)
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
        required=False,
    )
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )
    age = forms.ChoiceField(label="Age",
                            choices=AGE_RANGES)
    phone = forms.CharField(label="Primary Phone #:", max_length=200)
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
        label="Devilery/Distribution",
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
    # seriously?
    photo_release = forms.BooleanField(
        label="Do you accept the Photo Release?", required=False)
    opt_in = forms.BooleanField(label="", required=False)

    def save(self, *args, **kwargs):
        saved = super(ProfileUpdateForm, self).save(*args, **kwargs)
        try:
            saved.user.email = self.data.get('email')
            saved.user.save()
        except:
            pass
        if 'vt_counties' in self.data:
            for pk in self.data.getlist('vt_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
                county.affix_to_memorgs(saved.user)
        if 'ny_counties' in self.data:
            for pk in self.data.getlist('ny_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
                county.affix_to_memorgs(saved.user)
        return saved

    class Meta:
        model = Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('member_organization',)


class AdminProfileForm(EditProfileForm):

    def save(self, *args, **kwargs):
        super(AdminProfileForm, self).save()

    class Meta:
        model = Profile
        fields = ('first_name',
                  'last_name',
                  'address_one',
                  'address_two',
                  'city',
                  'state',
                  'zipcode',
                  'counties',
                  'phone',
                  'phone_type',
                  )

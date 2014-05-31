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
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div style='float: right'>"),
            Fieldset(
                "",
                Row("password1"),
                Row("password2")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='change password'>"),
            HTML("</div>"),
            Fieldset(
                "",
                Row("first_name", "last_name"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode", "age"),
                Row("phone", "phone_type"),
                Row("email", "preferred_method")
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
                HTML("<h3 class='lbl'>Change Releases</h3>"
                     "<h4>If you wish to change your stance"
                     "on recieving emails or if photos of you"
                     "get used, this is the place</h4>"),
                AppendedText('photo_release', '<h4>I accept the <strong>'
                             'Photo Release</strong></h4>'),
                AppendedText('opt_in', '<h4 style="text-align:left">Keep me'
                             ' in the loop!</h4>'
                             '<h5>(with periodic email updates &amp;'
                             ' newsletters from Salvation Farms)</h5>'),

                HTML("<br /><p>By having become a member you have accepted the"
                     " <u><b>Waiver of Liability</b></u> and<br /><u><b>Waiver"
                     " of Liability</b></u>. These are required for your cont"
                     "inued participation in <br />the Vermont Gleaning Colle"
                     "ctive efforts.</p>"),
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
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
    email = forms.EmailField(label="Email", max_length=200, required=False)
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
    photo_release = forms.BooleanField(
        label="", required=False)
    opt_in = forms.BooleanField(label="", required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Change Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=False)

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
        if 'ny_counties' in self.data:
            for pk in self.data.getlist('ny_counties'):
                county = County.objects.get(pk=pk)
                saved.counties.add(county)
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


class AdminProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-admin-registration-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div style='float: right'>"),
            Fieldset(
                "",
                Row("password1"),
                Row("password2")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='change password'>"),
            HTML("</div>"),
            Fieldset(
                "",
                Row("first_name", "last_name"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode"),
                HTML("<h3 class='lbl'>Counties</h3>"),
                Div(InlineCheckboxes("vt_counties"),
                    InlineCheckboxes("ny_counties"),
                    css_class="form-checkboxes"),
                Row("phone", "phone_type"),
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
        )
        profile = kwargs["instance"]
        self.initial["vt_counties"] = [
            x.pk for x in profile.counties.filter(state="VT")
        ]
        self.initial["ny_counties"] = [
            x.pk for x in profile.counties.filter(state="NY")
        ]

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
        required=False,
    )
    ny_counties = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=County.objects.filter(state="NY").order_by("name"),
        label="Counties in New York",
        required=False
    )
    phone = forms.CharField(label="Primary Phone #:", max_length=200)
    phone_type = forms.ChoiceField(
        label="Phone Type", choices=PHONE_TYPE, initial='1')
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Change Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=False)


    def save(self, *args, **kwargs):
        saved = super(AdminProfileForm, self).save(*args, **kwargs)
        saved.user.save()
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
        model = Profile
        exclude = ('member_organization', 'ecfirst_name', 'preferred_method',
                   'ecrelationship', 'ecphone', 'eclast_name',)


class UserEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_errors = False
        self.helper.form_id = "id-custom-admin-edit-form"
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            HTML("<div style='float: right'>"),
            Fieldset(
                "",
                Row("password1"),
                Row("password2")
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='change password'>"),
            HTML("</div>"),
            Fieldset(
                "",
                Row("first_name", "last_name"),
                Row("address_one", "address_two"),
                Row("city", "state"),
                Row("zipcode", "age"),
                Row("phone", "phone_type"),
                Row("email", "preferred_method")
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
                HTML("<h3 class='lbl'>Change Releases</h3>"
                     "<h4>If you wish to change your stance"
                     "on recieving emails or if photos of you"
                     "get used, this is the place</h4>"),
                AppendedText('photo_release', '<h4>I accept the <strong>'
                             'Photo Release</strong></h4>'),
                AppendedText('opt_in', '<h4 style="text-align:left">Keep me'
                             ' in the loop!</h4>'
                             '<h5>(with periodic email updates &amp;'
                             ' newsletters from Salvation Farms)</h5>'),

                HTML("<br /><p>By having become a member you have accepted the"
                     " <u><b>Waiver of Liability</b></u> and<br /><u><b>Waiver"
                     " of Liability</b></u>. These are required for your cont"
                     "inued participation in <br />the Vermont Gleaning Colle"
                     "ctive efforts.</p>"),
            ),
            HTML("<input type='submit' "
                 "class='glean-button green-button' "
                 "name='submit' value='Save Changes'>")
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
    photo_release = forms.BooleanField(
        label="", required=False)
    opt_in = forms.BooleanField(label="", required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Change Password", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", required=False)

    def save(self, *args, **kwargs):
        saved = super(UserEditForm, self).save(*args, **kwargs)
        try:
            saved.user.email = self.data.get('email')
            saved.user.save()
        except:
            pass
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
        model = Profile

from django.db import models
from django.contrib.auth.models import User
from django import forms
#from registration.forms import RegistrationForm
#from registration.backends.default import DefaultBackend

from constants import AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, TASKS, STATES

from counties.models import County
from memberorgs.models import MemOrg
from gleanevent.models import PostGlean


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        blank=True,
        unique=True,
        editable=False,
        related_name="profile"
    )

    first_name = models.CharField("First Name", max_length=20)
    last_name = models.CharField("Last Name", max_length=20)
    address_one = models.CharField(
        "Address (line one)", max_length=200, blank=True, null=True)
    address_two = models.CharField(
        "Address (line two)", max_length=200, blank=True, null=True)
    city = models.CharField("City", max_length=200, blank=True)
    state = models.CharField(
        "State", max_length=2, choices=STATES, default='VT')
    zipcode = models.CharField("Zipcode", max_length=11, blank=True, null=True)
    counties = models.ManyToManyField(
        County, blank=True, null=True, related_name='people')
    age = models.CharField("Age", max_length=200,
                           choices=AGE_RANGES,
                           blank=True)
    phone = models.CharField("Primary Phone", max_length=200, blank=True)
    phone_type = models.CharField(
        "Phone Type", choices=PHONE_TYPE, max_length=1, default='1')
    mo_emails_only = models.BooleanField(
        default=False, editable=False)
    preferred_method = models.CharField(
        choices=PREFERRED_CONTACT, max_length=1, default='1')
    member_organization = models.ForeignKey(
        MemOrg, blank=True, null=True, editable=False)

    joined = models.DateTimeField(
        auto_now_add=True, editable=False, null=True)

    ecfirst_name = models.CharField(
        "Emergency Contact First Name", max_length=200)
    eclast_name = models.CharField(
        "Emergency Contact Last Name", max_length=200)
    ecphone = models.CharField("Emergency Contact Phone", max_length=200)
    ecrelationship = models.CharField("Relationship", max_length=200)

    rsvped = models.IntegerField(editable=False, default=0)
    attended = models.IntegerField(editable=False, default=0)
    hours = models.DecimalField(
        editable=False, null=True, max_digits=4, decimal_places=2, default=0)

    accepts_email = models.BooleanField(default=True, editable=False)
    unsubscribe_key = models.CharField(
        "Unsubscribe key, for emails",
        max_length=30,
        blank=True,
        null=True,
        editable=False
        )
    tasks_gleaning = models.BooleanField(
        "Field Gleaning",
        default=True
    )
    tasks_farm_pickups = models.BooleanField(
        "Farmers Market/Farm Pick-ups",
        default=False
    )
    tasks_delivery = models.BooleanField(
        "Devilery/Distribution",
        default=False
    )
    tasks_admin = models.BooleanField(
        "Administrative Support",
        default=False
    )
    tasks_processing = models.BooleanField(
        "Processing",
        default=False
    )
    notes = models.TextField(
        verbose_name="Please share a little bit about yourself:",
        null=True
    )
    waiver = models.BooleanField(
        "Do you agree to the Waiver of Liability?", default=False)
    agreement = models.BooleanField(
        "Do you agree to the Volunteer Agreement?", default=False)
    photo_release = models.BooleanField(
        "Do you consent to the Photo Release?", default=False)
    opt_in = models.BooleanField(
        "Would you like to recieve additional newsletters and personal"
        " messages from the Gleaning Cooperative?", default=False)

    not_notified = models.BooleanField(editable=False, default=True)

    def get_hours(self):
        pgs = PostGlean.objects.filter(user=self.user)
        total = 0
        for pg in pgs:
            total += pg.hours
        return total

    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.user)

    class Meta:
        permissions = (
            ("auth", "Member Organization Level Permissions"),
            ("promote", "Ability to Promote Users"),
            ("uniauth", "Universal Permission Level"),
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('member_organization',)


class AdminProfileForm(EditProfileForm):
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


class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(
        max_length=50, widget=forms.widgets.PasswordInput)
    verify = forms.CharField(max_length=50, widget=forms.widgets.PasswordInput)
    email = forms.EmailField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(
        max_length=50, widget=forms.widgets.PasswordInput)


class EmailForm(forms.Form):
    email = forms.EmailField()


class UniPromoteForm(forms.Form):
    member_organization = forms.ModelChoiceField(
        queryset=MemOrg.objects.all(), label="Member Organization")
    promote = forms.BooleanField(
        label="Confirm Administrator Privileges", required=False)
    executive = forms.BooleanField(
        label="Confirm Additional Program Director Privileges", required=False)


class PromoteForm(forms.Form):
    promote = forms.BooleanField(
        label="Are you sure you want to promote "
        "this person to Glean Coordinator?", required=False)

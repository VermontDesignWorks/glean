import random

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models

from constants import AGE_RANGES, PHONE_TYPE, PREFERRED_CONTACT, TASKS, STATES

from counties.models import County
from memberorgs.models import MemOrg


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
    city = models.CharField("City", max_length=200, blank=True, null=True)
    state = models.CharField(
        "State", max_length=2, choices=STATES, default='VT', null=True)
    zipcode = models.CharField("Zipcode", max_length=11, blank=True, null=True)
    counties = models.ManyToManyField(
        County, blank=True, null=True, related_name='people')
    age = models.CharField("Age", max_length=200,
                           choices=AGE_RANGES,
                           blank=True,
                           null=True)
    phone = models.CharField(
        "Primary Phone",
        max_length=200,
        blank=True,
        null=True
    )
    phone_type = models.CharField(
        "Phone Type", choices=PHONE_TYPE, max_length=1, default='1', null=True)
    mo_emails_only = models.BooleanField(
        default=False, editable=False)
    preferred_method = models.CharField(
        choices=PREFERRED_CONTACT, max_length=1, default='1', null=True)
    member_organization = models.ForeignKey(
        MemOrg, blank=True, null=True, editable=False)

    joined = models.DateTimeField(
        auto_now_add=True, editable=False, null=True)

    ecfirst_name = models.CharField(
        "Emergency Contact First Name", max_length=200, null=True)
    eclast_name = models.CharField(
        "Emergency Contact Last Name", max_length=200, null=True)
    ecphone = models.CharField(
        "Emergency Contact Phone",
        max_length=200,
        null=True
    )
    ecrelationship = models.CharField(
        "Relationship",
        max_length=200,
        null=True
    )
    rsvped = models.IntegerField(editable=False, default=0, null=True)
    attended = models.IntegerField(editable=False, default=0, null=True)
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
        default=False
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
        null=True,
        blank=True
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

    def __unicode__(self):
        return u'%s %s %s' % (self.first_name, self.last_name, self.user)

    def notify_registration(self):
        notified = []
        for county in self.counties.all():
            if county.member_organizations.all():
                for memo in county.member_organizations.all():
                    if memo not in notified:
                        notified.append(memo)
                        memo.notify_admin(self.user)
            else:
                memo = MemOrg.objects.get(pk=1)
                if memo not in notified:
                    notified.append(memo)
                    memo.notify_admin(self.user)
        return notified

    @property
    def admin(self):
        if hasattr(self.user, "groups"):
            if self.user.groups.exists():
                return True
        return False

    @property
    def _unsubscribe_key(self):
        if not self.unsubscribe_key:
            value = ''
            for i in range(29):
                value += random.choice('abcdefghijklmnopqrstuvwvyz')
            self.unsubscribe_key = value
            self.save()
        return self.unsubscribe_key

    @property
    def unsubscribe_url(self):
        site = Site.objects.get(pk=1)
        key = self._unsubscribe_key
        return "http://{0}{1}".format(
            site.domain,
            reverse('announce:unsubscribelink', args=(key,))
        )

    class Meta:
        permissions = (
            ("auth", "Member Organization Level Permissions"),
            ("promote", "Ability to Promote Users"),
            ("uniauth", "Universal Permission Level"),
        )

    @property
    def stock_unsubscribe_link(self):
        """Crease a generic unsubscribe anchor tag, HTML ready"""
        return """
        <a href='{0}'>Click Here to Unsubscribe</a>
        (If the link doesn't work, copy and paste the following address
        into your browser: {0} )
        """.format(
            self.unsubscribe_url,
        )

    @property
    def accepts_gleans(self):
        if self.tasks_gleaning and self.accepts_email:
            return True
        return False


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

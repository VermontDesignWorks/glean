from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string

from counties.models import County

from constants import STATES, LINE_TYPE, ACCESS_LEVELS, COLORS
from mail_system import quick_mail


class MemOrg(models.Model):
    name = models.CharField(max_length=200)
    website = models.CharField('Website', max_length=50, blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
    counties = models.ManyToManyField(
        County,
        blank=True,
        null=True,
        related_name="member_organizations"
    )
    created = models.DateTimeField(auto_now_add=True)
    color = models.CharField(
        'Color', choices=COLORS, max_length=20, default='muted')

    address_one = models.CharField(
        'Physical Address (line one)', max_length=30, blank=True, null=True)
    address_two = models.CharField(
        'Physical Address (line two)', max_length=30, blank=True, null=True)
    city = models.CharField('City', max_length=15, blank=True, null=True)
    state = models.CharField(
        "State", choices=STATES, default="VT", max_length=2, blank=True)
    zipcode = models.CharField(
        "Zipcode", max_length=11, blank=True, null=True)
    physical_is_mailing = models.BooleanField(
        'Physical Address is Mailing Address', default=True)

    mailing_address_one = models.CharField(
        'Mailing Address (line one)', max_length=200, blank=True)
    mailing_address_two = models.CharField(
        'Mailing Address (line two)', max_length=200, blank=True)
    mailing_city = models.CharField(
        'Mailing Address (City)', max_length=200, blank=True)
    mailing_state = models.CharField(
        'Mailing Address (State)', choices=STATES, max_length=2, blank=True)
    mailing_zip = models.CharField(
        'Mailing Address Zipcode', max_length=11, blank=True)

    phone_1 = models.CharField(
        'Primary phone', max_length=200, blank=True)
    phone_1_type = models.CharField(
        'Primary Phone Type', choices=LINE_TYPE, max_length=10, blank=True)
    phone_2 = models.CharField(
        'Secondary phone', max_length=200, blank=True)
    phone_2_type = models.CharField(
        'Secondary Phone Type', choices=LINE_TYPE, max_length=10, blank=True)

    first_name = models.CharField(
        "Executive Director First Name", max_length=20, blank=True)
    last_name = models.CharField(
        "Executive Director Last Name", max_length=20, blank=True)
    phone = models.CharField(
        "Director's Direct Phone Number", max_length=15, blank=True, null=True)

    notify = models.BooleanField(
        'Notify on New Volunteer Signup?', default=False)

    testing = models.BooleanField(
        "Relay Announcement Emails to Testing Address", default=True)

    testing_email = models.CharField(
        "Primary Email Address", max_length="200", blank=True, null=True)

    notification_email = models.CharField(
        "Primary Email Address", max_length="200", blank=True, null=True)

    def __unicode__(self):
        return self.name

    def notify_admin(self, user):
        if self.notify and self.notification_email:
            subject = "New User Notification"
            text = render_to_string(
                "registration/notify.html",
                {"object": user.profile, "member_organization": self}
            )
            quick_mail(subject, text, self.notification_email)
            return 1
        else:
            return 0

    def create_default_template(self):
        """Creates initial, default template for Member Org"""
        from announce.models import Template
        query = Template.objects.filter(
            member_organization=self,
            default=True,
        )
        if not query.exists():
            f = file("announce/templates/announce/default_email.html")
            body = f.read()
            f.close()
            return Template.objects.create(
                template_name="Default Template for {0}".format(self.name),
                member_organization=self,
                body=body,
                default=True
            )
        return None

    @property
    def default_template(self):
        if self.templates.filter(default=True):
            return self.templates.filter(default=True)[0]
        return self.create_default_template()

    class Meta:
        permissions = (
            ("auth", "Member Organization Level Permissions"),
            ("uniauth", "Universal Permission Level"),
        )


class MemOrgForm(forms.ModelForm):
    class Meta:
        model = MemOrg


class NewAdminForm(forms.Form):
    member_organization = forms.ModelChoiceField(
        queryset=MemOrg.objects.all(), empty_label=None)
    access_level = forms.ChoiceField(choices=ACCESS_LEVELS, required=False)
    username = forms.CharField(max_length=20, required=False)
    password = forms.CharField(max_length=50, required=False)
    verify = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=20, required=False)

admin.site.register(MemOrg)

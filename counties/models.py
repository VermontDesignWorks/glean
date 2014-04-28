from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from django.template.loader import render_to_string

#from userprofile.models import Profile

from mail_system import quick_mail
from constants import STATES
# Create your models here.


class County(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    towns = models.TextField(max_length=200, blank=True)
    state = models.CharField(choices=STATES, max_length=2, default='VT')

    class Meta:
        permissions = (
            ("uniauth", "Universal Permission Level"),
            )

    def affix_to_memorgs(self, user, mail=False):
        profile = user.profile
        orgs = self.memorg_set.all()
        subject = "New User Registered in " + self.name
        text = render_to_string(
            "registration/notify.html",
            {"object": profile, "county": self}
        )
        for org in orgs:
            if mail and org.notify:
                email = getattr(org, "testing_email", False)
                if email:
                    quick_mail(subject, text, org.testing_email)
            org.volunteers.add(user)

    def __unicode__(self):
        return self.name


class CountyForm(ModelForm):
    class Meta:
        model = County

admin.site.register(County)

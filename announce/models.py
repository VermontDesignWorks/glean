import datetime
from django.utils import timezone

from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User

from gleanevent.models import GleanEvent
from memberorgs.models import MemOrg

from functions import primary_source


class Template(models.Model):
	template_name = models.CharField(max_length=40)
	member_organization = models.ForeignKey(MemOrg, editable=False)
	body = models.TextField()
	default = models.BooleanField(default=False)

	def __unicode__(self):
		return self.member_organization.name + ' - ' + self.template_name

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

class TemplateForm(ModelForm):
	class Meta:
		model = Template

class PartialTemplateForm(ModelForm):
	class Meta:
		model = Template
		exclude = ('template_name')

class Announcement(models.Model):
	email_recipients = models.ManyToManyField(User, null=True, blank=True, related_name="invitees", editable=False)
	phone_recipients = models.ManyToManyField(User, null=True, blank=True, related_name="Phone List", editable=False)
	datetime = models.DateTimeField(auto_now_add=True, editable=False)
	glean = models.ForeignKey(GleanEvent, blank=True, null=True, editable=False)
	title = models.CharField("Add a Custom Subject", max_length=50, null=True, blank=True)
	message = models.TextField("Add a Custom Message",null=True, blank=True)
	template = models.ForeignKey(Template, null=True, verbose_name="Email Template")
	sent = models.BooleanField(default=False, editable=False)
	sent_by = models.ForeignKey(User, editable=False, null=True)
	member_organization = models.ForeignKey(MemOrg, editable=False, verbose_name="Member Organization")

	class Meta:
		permissions = (
			("auth", "Member Organization Level Permissions"),
			("uniauth", "Universal Permission Level"),
		)

	def __unicode__(self):
		return self.datetime.strftime('%y:%m:%d %H:%M:%S') + self.member_organization.name

	def active(self):
		if self.datetime + datetime.timedelta(hours=3) >= timezone.now():
			return True
		else:
			return False

	def populate_recipients(self):
		self.email_recipients.clear()
		self.phone_recipients.clear()
		source = primary_source(self.glean)
		for county in source.counties.all():
			for recipient in county.people.all():
				if recipient.accepts_email:
					if recipient.preferred_method == '1':
						self.email_recipients.add(recipient.user)
					else:
						self.phone_recipients.add(recipient.user)

	def uninvite_user(self, user):
		if user in self.email_recipients.all():
			self.email_recipients.remove(user)
		if user in self.phone_recipients.all():
			self.phone_recipients.remove(user)

class AnnouncementForm(ModelForm):
	class Meta:
		model = Announcement
		

class RsvpModel(models.Model):
	key = models.CharField(max_length=25, primary_key=True)
	user = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)

class UnsubscribeModel(models.Model):
	key = models.CharField(max_length=25, primary_key=True)
	user = models.ForeignKey(User)

class RecipientList(models.Model):
	announcement = models.ForeignKey(Announcement)
	recipients = models.ManyToManyField(User)

	def __unicode__(self):
		return str(self.id) + " Recipient List " 
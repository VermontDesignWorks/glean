from django.contrib import admin
from django.db import models
from django.forms import ModelForm

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

	def affix_to_memorgs(self,user):
		profile = user.profile_set.get()
		orgs = self.memorg_set.all()
		sent= []
		subject = "New User Registered in " + self.name 
		text = "<html><head><title>New User</title></head><body><h3>New User Joined in %s</h3><p>%s %s (%s) has signed up to glean in %s.</p><p style='font-size:0.8em'>You are recieving this notification because you opted into notifications when new volunteers joined in counties your Member Organization gleans in. To stop recieving these notifications, sign into the Gleaners Interface and change your Member Organization preferences.</p></body></html>" % (self.name, profile.first_name, profile.last_name, user.email, self.name)
		for org in orgs:
			if org.notify == True:
				for person in org.profile_set.all():
					if person.user.has_perm('userprofile.promote') and person.user not in sent:
						
						quick_mail(subject, text, person.user)
						sent.append(person.user)
			org.volunteers.add(user)

	def __unicode__(self):
		return self.name

class CountyForm(ModelForm):
	class Meta:
		model = County

admin.site.register(County)
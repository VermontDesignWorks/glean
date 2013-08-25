## -- Time to Split -- ##
import sys
import random

from django.core.urlresolvers import reverse

from django.http import HttpResponse

from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from functions import primary_source

def weave_template_and_body_and_glean(template, announcement, glean):
	site = Site.objects.get(pk=1)
	glean_link = "<a href='" + site.domain + str(reverse('gleanevent:detailglean', args=(glean.id,))) + "'>Glean Info</a>"
	replace = {
		'{{custom}}':announcement.message,
		'{{glean.title}}':glean.title, 
		'{{glean.description}}':glean.description,
		#'{{info}}':glean_link,
	}
	returnable = template.body
	for key, value in replace.iteritems():
		if returnable.find(key) != -1:
			try:
				start = returnable.find(key)
				finish = returnable.find(key)+len(key)
				returnable = returnable[:start] + value + returnable[finish:]
			except: #in the case that the key ends the document
				start = returnable.find(key)
				finish = returnable.find(key)+len(key)
				returnable = returnable[:start] + value
	return returnable

def weave_unsubscribe(body, userprofile, announce):
	site = Site.objects.get(pk=1)
	returnable = body
	key = '{{unsubscribe}}'
	if userprofile.unsubscribe_key:
		value = userprofile.unsubscribe_key
	else:
		value = ''
		for i in range(29):
			value += random.choice('abcdefghijklmnopqrstuvwvyz')
		userprofile.unsubscribe_key = value
		userprofile.save()
	unsub_link = "<a href='" + site.domain+ str(reverse('announce:unsubscribelink', args=(value,)))+"'>Click Here Unsubscribe</a> (if the link doesn't work, copy and paste the following address into your browser: " + site.domain+ str(reverse('announce:unsubscribelink', args=(value,)))
	glean_link = "<a href='" + site.domain + str(reverse('gleanevent:detailglean', args=(announce.glean.id,))) + "'>Glean Time and Location Information</a>"
	raw_glean_link = site.domain+str(reverse('gleanevent:detailglean', args=(announce.glean.id,)))
	if announce.title:
		subject = announce.title
	else:
		subject = announce.glean.title
	replace = {
		'{{custom}}':announce.message,
		'{{glean.title}}':announce.glean.title, 
		'{{glean.description}}':announce.glean.description,
		'{{info}}':glean_link,
		'{{raw_glean_link}}':raw_glean_link,
		'{{unsubscribe}}': unsub_link,
		'{{subject}}':subject,
	}
	returnable = announce.template.body
	for key, value in replace.iteritems():
		if returnable.find(key) != -1:
			try:
				start = returnable.find(key)
				finish = returnable.find(key)+len(key)
				returnable = returnable[:start] + value + returnable[finish:]
			except: #in the case that the key ends the document
				start = returnable.find(key)
				finish = returnable.find(key)+len(key)
				returnable = returnable[:start] + value
	return returnable


#== Mailing Logic ==#
def quick_mail(subject, text, recipient):
	msg = EmailMessage(subject, text, 'The Gleaners Interface', [recipient.email])
	msg.content_subtype = "html"
	msg.send()

def mail_from_source(body, announcement):
		if announcement.title:
			subject = announcement.title
		else:
			subject = announcement.glean.title
		counter = 0
		for recipient in announcement.email_recipients.all():
			rprofile = recipient.profile_set.get()
			text = weave_unsubscribe(body,rprofile,announcement)
			msg = EmailMessage(subject, text, 'The Gleaners Interface', [recipient.email])
			msg.content_subtype = "html"
			msg.send()
			if recipient not in announcement.glean.invited_volunteers.all():
				announcement.glean.invited_volunteers.add(recipient)
		for recipient in announcement.phone_recipients.all():
			if recipient not in announcement.glean.invited_volunteers.all():
				announcement.glean.invited_volunteers.add(recipient)
		announcement.glean.save()
	

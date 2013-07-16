# Create your views here.
import time
import datetime
import random

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required


from announce.models import Template, TemplateForm, Announcement, AnnouncementForm, PartialTemplateForm
from gleanevent.models import GleanEvent
from userprofile.models import Profile

from django.core.mail import send_mail


def recipients_placeholder_code():
	return Profile.objects.all()

def primary_source(glean):
	if hasattr(glean,'counties'):
		return glean
	elif hasattr(glean.farm_location.counties):
		return glean.farm_location
	elif hasattr(glean.farm.counties):
		return glean.farm



#==================== Template System ====================#

def Templates(request):
	templates = Template.objects.all()
	return render(request, 'announce/templates.html', {'templates':templates})

def editTemplate(request, template_id):
	template = get_object_or_404(Template, pk=template_id)
	if request.method == 'POST':
		form = PartialTemplateForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['body'].find('{{content}}') != -1:
				template.body = form.cleaned_data['body']
				template.save()
				return HttpResponseRedirect(reverse('announce:templates'))
			else:
				form = PartialTemplateForm(instance=newTemplate)
				return render(request, 'announce/edit_template.html', {'form':form, 'template':template, 'error':'Need a {{content}} tag!', 'editmode':True})
		else:
			return render(request, 'announce/edit_template.html', {'form':form, 'template':template, 'error':'Form was not valid', 'editmode':True})
	else:		
		form = PartialTemplateForm(instance=template)
		return render(request, 'announce/edit_template.html', {'form':form, 'template':template})

def newTemplate(request):
	if request.method == 'POST':
		form = TemplateForm(request.POST)
		if form.is_valid():
			newTemplate = Template(**form.cleaned_data)
			if form.cleaned_data['body'].find('{{content}}') != -1:
				newTemplate.save()
				return HttpResponseRedirect(reverse('announce:templates'))
			else:
				form = TemplateForm(instance=newTemplate)
				return render(request, 'announce/new_template.html', {'form':form, 'error':'Need a {{content}} tag!'})
		else:
			return HttpResponse('form is not valid')
	else:
		form = TemplateForm
		return render(request, 'announce/new_template.html', {'form':form})

def detailTemplate(request, template_id):
	template = get_object_or_404(Template, pk=template_id)
	return render(request, 'announce/template_detail.html', {'template':template})


#==================== Announce Logic ====================#

def weave_template_and_body_and_glean(template, announcement, glean):
	glean_link = "<a href='" + str(reverse('gleanevent:detailglean', args=(glean.id,))) + "'>Glean Info</a>"
	replace = {
		'{{content}}':announcement.message,
		'{{glean.title}}':glean.title, 
		'{{glean.description}}':glean.description,
		'{{info}}':glean_link,
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

def weave_unsubscribe(body, userprofile):
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
	value = "<a href='" + str(reverse('announce:unsubscribelink', args=(value,)))+"'>Unsubscribe</a>"

	if body.find(key) != -1:
		try:
			start = returnable.find(key)
			finish = returnable.find(key)+len(key)
			returnable = returnable[:start] + value + returnable[finish:]
		except: #in the case that the key ends the document
			start = returnable.find(key)
			finish = returnable.find(key)+len(key)
			returnable = returnable[:start] + value
	return returnable

def mail_from_source(source, body, announcement):
	mailed = []
	for county in source.counties.all():
		for recipient in county.people.all():
			if recipient not in mailed and recipient.accepts_email:
				text = weave_unsubscribe(body,recipient)
				send_mail(announcement.title, text, 'Salvation Farms', [recipient.user.email], fail_silently=False)
				if recipient not in announcement.glean.invited_volunteers.all():
					announcement.glean.invited_volunteers.add(recipient.user)
				mailed.append(recipient)
	announcement.glean.save()

#==================== Announce System ====================#

def detailAnnounce(request, announce_id):
	announcement = get_object_or_404(Announcement, pk=announce_id)
	body = weave_template_and_body_and_glean(announcement.template, announcement, announcement.glean)
	glean = announcement.glean
	source = primary_source(announcement.glean)
	if request.method == 'POST' and announcement.sent == False:
		mail_from_source(source, body, announcement)
		# mailed = []
		# for county in source.counties.all():
		# 	for recipient in county.people.all():
		# 		if recipient not in mailed:
		# 			send_mail(announcement.title, test, 'Salvation Farms', [recipient.user.email], fail_silently=False)
		# 			mailed.append(recipient)
		announcement.sent = True
		announcement.save()
		return HttpResponseRedirect(reverse('announce:detailannounce', args=(announce_id,)))
	else:
		
		return render(request, 'announce/announce_detail.html', {'announcement':announcement, 'test':body, 'glean':glean, 'source':source})

def Announcements(request):
	announcements = Announcement.objects.all()
	return render(request, 'announce/announcements.html', {'announcements':announcements})

def announceGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if not glean.happened():
		if request.method == 'POST':
			form = AnnouncementForm(request.POST)
			if form.is_valid():
				newAnnounce = Announcement(**form.cleaned_data)
				newAnnounce.glean = glean
				newAnnounce.save()
				return HttpResponseRedirect(reverse('announce:detailannounce', args=(newAnnounce.id,)))
			else:
				HttpResponse('form was not vaild')
		else:
			templates = Template.objects.all()
			form = AnnouncementForm()
			source = primary_source(glean)
			return render(request, 'announce/announce.html', {'glean':glean, 'templates':templates, 'form':form, 'source':source})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id)))

def editAnnounce(request, announce_id):
	announce = get_object_or_404(Announcement, pk=announce_id)
	templates = Template.objects.all()
	recipients = recipients_placeholder_code()
	if request.method == 'POST':
		form = AnnouncementForm(request.POST)
		if form.is_valid():
			newAnnounce = Announcement(**form.cleaned_data)
			newAnnounce.glean = announce.glean
			newAnnounce.id = announce.id
			newAnnounce.datetime = announce.datetime
			newAnnounce.save()
			return HttpResponseRedirect(reverse('announce:detailannounce', args=(newAnnounce.id,)))
		else:
			return render(request, 'announce/edit_announce.html', {'glean':announce.glean, 'templates':templates, 'form':form, 'recipients':recipients, 'editmode':True})
	else:
		templates = Template.objects.all()
		form = AnnouncementForm(instance=announce)
		recipients = recipients_placeholder_code()
		return render(request, 'announce/edit_announce.html', {'glean':announce.glean, 'templates':templates, 'form':form, 'recipients':recipients, 'editmode':True})



#==================== Single Use Links ====================#

def unsubscribeLink(request, key):
	prof = get_object_or_404(Profile, unsubscribe_key=key)
	prof.accepts_email = False
	prof.unsubscribe_key = None
	prof.save()
	return render(request, 'announce/unsubscribe.html')

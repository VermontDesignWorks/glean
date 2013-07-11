# Create your views here.
import time
import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required


from announce.models import Template, TemplateForm, Announcement, AnnouncementForm, PartialTemplateForm
from gleanevent.models import GleanEvent
from userprofile.models import Profile


def recipients_placeholder_code():
	return Profile.objects.all()

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
		#'{{rsvp}}':
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





#==================== Announce System ====================#

def Announcements(request):
	announcements = Announcement.objects.all()
	return render(request, 'announce/announcements.html', {'announcements':announcements})

def announceGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
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
		recipients = recipients_placeholder_code()
		return render(request, 'announce/announce.html', {'glean':glean, 'templates':templates, 'form':form, 'recipients':recipients})

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


def detailAnnounce(request, announce_id):
	if request.method == 'POST':
		pass
	else:
		announcement = get_object_or_404(Announcement, pk=announce_id)
		test = weave_template_and_body_and_glean(announcement.template, announcement, announcement.glean)
		glean = announcement.glean
		recipients = recipients_placeholder_code()
		return render(request, 'announce/announce_detail.html', {'announcement':announcement, 'test':test, 'glean':glean, 'recipients':recipients})

#==================== Single Use Links ====================#

def rsvpLink(request, key):
	rsvp = get_object_or_404(rsvpModel, pk = key)
	glean = rsvp.glean
	user = rsvp.user
	glean.attending_volunteers.add(user)
	glean.save()
	return HttpResponseRedirect(reverse('gleanevent.detailglean', args=(glean.id,)))

def unsubscribeLink(request, key):
	NotImplementedError


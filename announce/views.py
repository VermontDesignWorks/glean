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
from django.contrib.auth.decorators import permission_required

from announce.models import Template, TemplateForm, Announcement, AnnouncementForm, PartialTemplateForm
from gleanevent.models import GleanEvent
from userprofile.models import Profile

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site

#==================== Recipient Logic ====================#

def primary_source(glean):
	if glean.counties.all():
		return glean
	elif glean.farm_location and glean.farm_location.counties.all():
		return glean.farm_location
	elif glean.farm and glean.farm.counties.all():
		return glean.farm
	else:
		return glean

#==================== Template System ====================#

#== Template Index  View==#
@permission_required('announce.auth')
def Templates(request):
	
	if request.user.has_perm('announce.uniauth'):
		templates = Template.objects.all()
	else:
		templates = Template.objects.filter(member_organization=request.user.profile_set.get().member_organization)	
	return render(request, 'announce/templates.html', {'templates':templates})

#== Template Edit View ==#
@permission_required('announce.auth')
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

#== Create New Template View ==#
@permission_required('announce.auth')
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

#== View for Individual Template ==#
@permission_required('announce.auth')
def detailTemplate(request, template_id):
	template = get_object_or_404(Template, pk=template_id)
	return render(request, 'announce/template_detail.html', {'template':template})


#==================== Announce Logic ====================#

#== Combine Template and Message for Emails ==#
def weave_template_and_body_and_glean(template, announcement, glean):
	site = Site.objects.get(pk=1)
	glean_link = "<a href='" + site.domain + str(reverse('gleanevent:detailglean', args=(glean.id,))) + "'>Glean Info</a>"
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

#== Final Weave, puts per-user unsubscribe link into email ==#
def weave_unsubscribe(body, userprofile):
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
	value = "<a href='" + site.domain+ str(reverse('announce:unsubscribelink', args=(value,)))+"'>Unsubscribe</a>"

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

#== Mailing Logic ==#
def mail_from_source(source, body, announcement):
	mailed = []
	for county in source.counties.all():
		for recipient in county.people.all():
			
			if recipient not in mailed and recipient.accepts_email and recipient.preferred_method == '1':
				mailed.append(recipient)
				text = weave_unsubscribe(body,recipient)
				msg = EmailMessage(announcement.title, text, 'Salvation Farms', [recipient.user.email])
				msg.content_subtype = "html"
				msg.send()
				#send_mail(announcement.title, text, 'Salvation Farms', [recipient.user.email], fail_silently=False)
				if recipient not in announcement.glean.invited_volunteers.all():
					announcement.glean.invited_volunteers.add(recipient.user)
				if recipient not in announcement.email_recipients.all():
					announcement.email_recipients.add(recipient.user)
			elif recipient.preferred_method == '2' and recipient.accepts_email:
				if recipient not in announcement.phone_recipients.all():
					announcement.phone_recipients.add(recipient.user)
	announcement.save()
	announcement.glean.save()

#==================== Announce System ====================#

#== View for individual Announcement ==#
@permission_required('announce.auth')
def detailAnnounce(request, announce_id):
	announcement = get_object_or_404(Announcement, pk=announce_id)
	if not request.user.has_perm('announce.uniauth') and request.user.profile_set.get().member_organization != announcement.member_organization:
		return HttpResponseRedirect(reverse('announce:announcements'))
	body = weave_template_and_body_and_glean(announcement.template, announcement, announcement.glean)
	glean = announcement.glean
	source = primary_source(announcement.glean)
	if request.method == 'POST' and announcement.sent == False:
		mail_from_source(source, body, announcement)
		announcement.sent = True
		announcement.sent_by = request.user
		announcement.save()
		return HttpResponseRedirect(reverse('announce:detailannounce', args=(announce_id,)))
	else:
		return render(request, 'announce/announce_detail.html', {'announcement':announcement, 'test':body, 'glean':glean, 'source':source})

#== View for Printable Phone List ==#
@permission_required('announce.auth')
def phoneAnnounce(request, announce_id):
	announcement = get_object_or_404(Announcement, pk=announce_id)
	if not request.user.has_perm('announce.uniauth') and request.user.profile_set.get().member_organization != announcement.member_organization:
		return HttpResponseRedirect(reverse('announce:announcements'))
	glean = announcement.glean
	source = primary_source(announcement.glean)
	return render(request, 'announce/phone.html', {'announcement':announcement, 'glean':glean, 'source':source})

#== Index of All Announcements ==#
@permission_required('announce.auth')
def Announcements(request):
	if request.user.has_perm('announce.uniauth'):
		announcements = Announcement.objects.all()
	else:
		announcements= Announcement.objects.filter(member_organization=request.user.profile_set.get().member_organization)
	return render(request, 'announce/announcements.html', {'announcements':announcements})
	#return HttpResponse(request.user.profile_set.get().member_organization)

#== New Announcement View ==#
@permission_required('announce.auth')
def announceGlean(request, glean_id):
	glean = get_object_or_404(GleanEvent, pk=glean_id)
	if not request.user.has_perm('announce.uniauth') and request.user.profile_set.get().member_organization != announce.member_organization:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id,)))
	if not glean.happened():
		if request.method == 'POST':
			form = AnnouncementForm(request.POST)
			if form.is_valid():
				new_save = form.save(commit=False)
				new_save.member_organization = glean.member_organization
				new_save.glean = glean
				new_save.save()
				return HttpResponseRedirect(reverse('announce:detailannounce', args=(new_save.id,)))
			else:
				HttpResponse('form was not vaild')
		else:
			templates = Template.objects.all()
			form = AnnouncementForm()
			source = primary_source(glean)
			return render(request, 'announce/announce.html', {'glean':glean, 'templates':templates, 'form':form, 'source':source})
	else:
		return HttpResponseRedirect(reverse('gleanevent:detailglean', args=(glean_id)))

#== Edit Announcement View ==#
@permission_required('announce.auth')
def editAnnounce(request, announce_id):
	announce = get_object_or_404(Announcement, pk=announce_id)
	if not request.user.has_perm('announce.uniauth') and request.user.profile_set.get().member_organization != announce.member_organization:
		return HttpResponseRedirect(reverse('announce:detailannounce', args=(announce_id,)))
	templates = Template.objects.all()
	source = primary_source(announce.glean)
	if request.method == 'POST':
		form = AnnouncementForm(request.POST)
		if form.is_valid():
			new_save = form.save(commit=False)
			new_save.member_organization = announce.member_organization
			new_save.glean = announce.glean
			new_save.datetime = announce.datetime
			new_save.id = announce.id
			new_save.save()
			return HttpResponseRedirect(reverse('announce:detailannounce', args=(new_save.id,)))
		else:
			return render(request, 'announce/edit_announce.html', {'glean':announce.glean, 'templates':templates, 'form':form, 'recipients':recipients, 'source':source})
	else:
		templates = Template.objects.all()
		form = AnnouncementForm(instance=announce)
		return render(request, 'announce/edit_announce.html', {'glean':announce.glean, 'templates':templates, 'form':form, 'recipients':recipients, 'source':source})



#==================== Single Use Links ====================#

#== Unsubscribe 'view' ==#
def unsubscribeLink(request, key):
	prof = get_object_or_404(Profile, unsubscribe_key=key)
	prof.accepts_email = False
	prof.unsubscribe_key = None
	prof.save()
	return render(request, 'announce/unsubscribe.html')

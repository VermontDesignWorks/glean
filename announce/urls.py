from django.conf.urls import patterns, url

from announce import views

urlpatterns = patterns('',
	
	#==================# Announce Urls #==================#
	url(r'^$', views.Announcements, name='announcements'),
	url(r'^(?P<glean_id>\d+)/new/$', views.announceGlean, name='announceglean'),
	url(r'^(?P<announce_id>\d+)/$', views.detailAnnounce, name='detailannounce'),
	url(r'^(?P<announce_id>\d+)/edit$', views.editAnnounce, name='editannounce'),
	url(r'^(?P<announce_id>\d+)/phone$', views.phoneAnnounce, name='phoneannounce'),

	#==================# Template Urls #==================#
	url(r'^templates/$', views.Templates, name='templates'),
	url(r'^templates/new/$', views.newTemplate, name='newtemplate'),
	url(r'^templates/(?P<template_id>\d+)', views.detailTemplate, name='detailtemplate'),
	url(r'^templates/edit/(?P<template_id>\d+)', views.editTemplate, name='edittemplate'),

	#=================# RSVP & Sub Urls #=================#
	url(r'^unsubscribe/(?P<key>\w+)$', views.unsubscribeLink, name='unsubscribelink'),
)
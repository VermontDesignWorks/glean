from django.conf.urls import patterns, url

from announce import views

urlpatterns = patterns(
    '',
    #==================# Announce Urls #==================#
    url(r'^$', views.AnnouncementListView.as_view(), name='announcements'),
    url(r'^(?P<glean_id>\d+)/new/$',
        views.announceGlean,
        name='announceglean'),
    url(r'^(?P<announce_id>\d+)/$',
        views.combinedAnnounce,
        name='combinedannounce'),
    url(r'^(?P<announce_id>\d+)/$',
        views.detailAnnounce,
        name='detailannounce'),
    url(r'^(?P<announce_id>\d+)/delete$',
        views.deleteAnnounce,
        name='deleteannounce'),
    url(r'^(?P<announce_id>\d+)/edit$',
        views.editAnnounce,
        name='editannounce'),
    url(r'^(?P<announce_id>\d+)/phone$',
        views.phoneAnnounce,
        name='phoneannounce'),
    url(r'^(?P<announce_id>\d+)/send$',
        views.sendAnnounce,
        name='sendannounce'),
    url(r'^(?P<announce_id>\d+)/htmlemail$',
        views.HTMLemail,
        name='htmlemail'),
    url(r'^(?P<announce_id>\d+)/remove/(?P<user_id>\d+)$',
        views.uninviteUser,
        name='uninviteuser'),
    url(r'^(?P<announce_id>\d+)/recipientlist$',
        views.recipientList,
        name='recipientlist'),


    #==================# Template Urls #==================#
    url(r'^templates/$', views.Templates, name='templates'),
    url(r'^templates/new/$', views.newTemplate, name='newtemplate'),
    url(r'^templates/(?P<template_id>\d+)/$',
        views.detailTemplate,
        name='detailtemplate'),
    url(r'^templates/(?P<template_id>\d+)/delete/$',
        views.deleteTemplate,
        name='deletetemplate'),
    url(r'^templates/(?P<pk>\d+)/edit/$',
        views.editTemplateClass.as_view(),
        name='edittemplate'),

    #=================# RSVP & Sub Urls #=================#
    url(r'^unsubscribe/(?P<key>\w+)$',
        views.unsubscribeLink,
        name='unsubscribelink'),
)

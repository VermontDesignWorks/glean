from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
	
	#==================# Announce Urls #==================#
	url(r'^farm/(?P<farm_id>[\w\s]+)/$', views.apiFarm, name='farm'),
	url(r'^farmlocation/(?P<farm_location_id>\d+)/$', views.apiFarmLocation, name='farmlocation'),
	)
from django.conf.urls import patterns, url

from distro import views


urlpatterns = patterns('',
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.entry, name='entry'),
	)
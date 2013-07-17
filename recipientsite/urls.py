from django.conf.urls import patterns, url

from recipientsite import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newSite, name='newsite'),
	url(r'^(?P<site_id>\d+)/$', views.detailSite, name='detailsite'),
	url(r'^(?P<site_id>\d+)/edit/$', views.editSite, name='editsite'),
)
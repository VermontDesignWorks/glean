from django.conf.urls import patterns, url

from counties import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newCounty, name='newcounty'),
	url(r'^(?P<county_id>\d+)/$', views.detailCounty, name='detailcounty'),
	url(r'^(?P<county_id>\d+)/edit/$', views.editCounty, name='editcounty'),
)
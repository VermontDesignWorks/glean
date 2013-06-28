from django.conf.urls import patterns, url

from farms import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newFarm, name='newfarm'),
	url(r'^(?P<farm_id>\d+)/$', views.detailFarm, name='detailfarm'),
	url(r'^(?P<farm_id>\d+)/edit/$', views.editFarm, name='editfarm'),
	url(r'^(?P<farm_id>\d+)/new/$', views.newLocation, name='newlocation'),
	url(r'^(?P<farm_id>\d+)/edit/location/(?P<location_id>\d+)/$', views.editLocation, name='editlocation')
)
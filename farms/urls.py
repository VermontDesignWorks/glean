from django.conf.urls import patterns, url

from farms import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newFarm, name='newfarm'),
	url(r'^download/$', views.download, name='download'),
	url(r'^(?P<farm_id>\d+)/$', views.detailFarm, name='detailfarm'),
	url(r'^(?P<farm_id>\d+)/edit/$', views.editFarm, name='editfarm'),
	url(r'^(?P<farm_id>\d+)/delete/$', views.deleteFarm, name='deletefarm'),

	url(r'^(?P<farm_id>\d+)/location/new/$', views.newLocation, name='newlocation'),
	url(r'^(?P<farm_id>\d+)/location/edit/(?P<location_id>\d+)/$', views.editLocation, name='editlocation'),
	url(r'^(?P<farm_id>\d+)/contact/new/$', views.newContact, name='newcontact'),
	url(r'^(?P<farm_id>\d+)/contact/edit/(?P<contact_id>\d+)/$', views.editContact, name='editcontact'),
)
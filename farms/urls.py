from django.conf.urls import patterns, url
from django.views.generic import View
from farms import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.NewFarm.as_view(), name='newfarm'),
    url(r'^download/$', views.download, name='download'),
    url(r'^(?P<farm_id>\d+)/$',
        views.detailFarm, name='detailfarm'),
    url(r'^(?P<pk>\d+)/edit/$',
        views.EditFarm.as_view(), name='editfarm'),
    url(r'^(?P<pk>\d+)/delete/$',
        views.DeleteFarm.as_view(), name='deletefarm'),
    url(r'^(?P<farm_id>\d+)/location/new/$',
        views.newLocation, name='newlocation'),
    url(r'^(?P<farm_id>\d+)/location/edit/(?P<pk>\d+)/$',
        views.EditLocation.as_view(), name='editlocation'),
    url(r'^(?P<farm_id>\d+)/contact/new/$',
        views.newContact, name='newcontact'),
    url(r'^(?P<farm_id>\d+)/contact/edit/(?P<contact_id>\d+)/$',
        views.editContact, name='editcontact'),
)

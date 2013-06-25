from django.conf.urls import patterns, url

from farms import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newFarm, name='newfarm'),
	url(r'^(?P<farm_id>\d+)/$', views.detailFarm, name='detailfarm'),
	url(r'^(?P<farm_id>\d+)/edit/$', views.editFarm, name='editfarm'),
)
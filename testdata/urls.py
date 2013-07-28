from django.conf.urls import patterns, url

from testdata import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^groups/$', views.groupsAndPerms, name='groupsandperms'),
	url(r'^delete/$', views.delete, name='delete'),
)
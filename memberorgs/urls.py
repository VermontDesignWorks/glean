from django.conf.urls import patterns, url

from memberorgs import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newMemOrg, name='newmemorg'),
	url(r'^(?P<memorg_id>\d+)/$', views.detailMemOrg, name='detailmemorg'),
	url(r'^(?P<memorg_id>\d+)/edit/$', views.editMemOrg, name='editmemorg'),
)
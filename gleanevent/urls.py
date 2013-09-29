from django.conf.urls import patterns, url

from gleanevent import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newGlean, name='newglean'),
	url(r'^download/$', views.download, name='download'),
	url(r'^postglean/download/$', views.postGleanDownload, name='postdownload'),
	url(r'^(?P<glean_id>\d+)/$', views.detailGlean, name='detailglean'),
	url(r'^(?P<glean_id>\d+)/edit/$', views.editGlean, name='editglean'),
	url(r'^(?P<glean_id>\d+)/print/$', views.printGlean, name='printglean'),
	url(r'^(?P<glean_id>\d+)/delete/$', views.deleteGlean, name='deleteglean'),
	url(r'^(?P<glean_id>\d+)/attending/$', views.confirmLink, name='confirmlink'),
	url(r'^(?P<glean_id>\d+)/notattending/$', views.denyLink, name='denylink'),
	url(r'^(?P<glean_id>\d+)/postglean/$', views.postGlean, name='postglean'),
	url(r'^(?P<glean_id>\d+)/viewpostglean/$', views.postGleanView, name='postgleanview'),
	url(r'^(?P<glean_id>\d+)/editpostglean/$', views.postGleanEdit, name='postgleanedit'),
)
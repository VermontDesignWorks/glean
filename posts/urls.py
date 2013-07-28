from django.conf.urls import patterns, url

from posts import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^new/$', views.newPost, name='newpost'),
	url(r'^(?P<post_id>\d+)/$', views.detailPost, name='detailpost'),
	url(r'^(?P<post_id>\d+)/edit$', views.editPost, name='editpost'),
)
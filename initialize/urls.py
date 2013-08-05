from django.conf.urls import patterns, url

from initialize import views

urlpatterns = patterns('',
	url(r'^$', views.create, name='create'),
)
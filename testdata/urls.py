from django.conf.urls import patterns, url

from testdata import views

try:
	import development
	urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^accounts/$', views.accounts, name='accounts'),
		url(r'^delete/$', views.delete, name='delete'),
	)
except:
	urlpatterns = patterns('',
		url(r'^$', views.redirect, name='redirect'),
		)
from django.conf.urls import patterns, url

from distro import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^entry/$', views.entry, name='entry'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^download/$', views.download, name='download'),
    url(r"^hours/$", views.WorkEventsCreateView.as_view(), name='hours')
    )

from django.conf.urls import patterns, url

from distro import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^entry/$', views.Entry.as_view(), name='entry'),
    url(r'^edit/$', views.Edit.as_view(), name='edit'),
    url(r'^download/$', views.download, name='download'),
    url(r"^hours/$", views.Hours_Entry.as_view(), name='hours')
    )

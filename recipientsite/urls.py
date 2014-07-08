from django.conf.urls import patterns, url

from recipientsite import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.NewSite.as_view(), name='newsite'),
    url(r'^(?P<site_id>\d+)/$', views.detailSite, name='detailsite'),
    url(r'^(?P<site_id>\d+)/edit/$', views.editSite, name='editsite'),
    url(r'^(?P<site_id>\d+)/delete/$', views.deleteSite, name='deletesite'),
)

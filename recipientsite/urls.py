from django.conf.urls import patterns, url

from recipientsite import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.NewSite.as_view(), name='newsite'),
    url(r'^(?P<pk>\d+)/$', views.DetailSite.as_view(), name='detailsite'),
    url(r'^(?P<pk>\d+)/edit/$', views.EditSite.as_view(), name='editsite'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteSite.as_view(), name='deletesite'),
)

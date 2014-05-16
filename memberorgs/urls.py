from django.conf.urls import patterns, url

from memberorgs import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.newMemOrg, name='newmemorg'),
    url(r'^(?P<pk>\d+)/$', views.DetailMemOrg.as_view(), name='detailmemorg'),
    url(r'^(?P<memorg_id>\d+)/edit/$', views.editMemOrg, name='editmemorg'),
    url(r'^(?P<memorg_id>\d+)/newadmin/$',
        views.newAdministrator,
        name='newadmin'),
)

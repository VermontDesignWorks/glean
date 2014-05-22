from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from memberorgs import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailMemOrg.as_view(), name='detailmemorg'),
    url(r'^new/$', views.NewMemOrg.as_view(), name='newmemorg'),
    url(r'^(?P<pk>\d+)/edit/$',  permission_required(
        'memberorgs.auth'
        )(views.EditMemOrg.as_view()),
        name='editmemorg'),
    url(r'^(?P<memorg_id>\d+)/newadmin/$',
        views.newAdministrator,
        name='newadmin'),
)

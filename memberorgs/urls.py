from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from memberorgs import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.newMemOrg, name='newmemorg'),
    url(r'^(?P<memorg_id>\d+)/$', views.detailMemOrg, name='detailmemorg'),
    url(r'^(?P<memorg_id>\d+)/edit/$', permission_required(
        'userprofile.auth'
        )(views.EditMemOrg.as_view()),
        name='editmemorg'),
    url(r'^(?P<memorg_id>\d+)/newadmin/$',
        views.newAdministrator,
        name='newadmin'),
)

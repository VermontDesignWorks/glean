from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required
from gleanevent import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$',
        permission_required(
            'gleanevent.auth'
        )(views.NewGlean.as_view()), name='newglean'),
    url(r'^(?P<pk>\d+)/edit/$',
        permission_required(
            'gleanevent.auth'
        )(views.UpdateGlean.as_view()), name='editglean'),
    url(r'^download/$', views.download, name='download'),
    url(r'^postglean/download/$',
        views.postGleanDownload,
        name='postdownload'),
    url(r'^(?P<glean_id>\d+)/$', views.detailGlean, name='detailglean'),
    url(r'^(?P<glean_id>\d+)/print/$', views.printGlean, name='printglean'),
    url(r'^(?P<glean_id>\d+)/delete/$', views.deleteGlean, name='deleteglean'),
    url(r'^(?P<glean_id>\d+)/attending/$',
        views.confirmLink,
        name='confirmlink'),
    url(r'^(?P<glean_id>\d+)/notattending/$', views.denyLink, name='denylink'),
)

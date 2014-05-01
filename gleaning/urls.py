from django.conf.urls import patterns, include, url
from customreg import MyRegistrationView
from django.contrib.auth import views as auth_views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'gleaning.views.home', name="home"),
    url(r'^glean/', include('gleanevent.urls', namespace="gleanevent")),
    url(r'^farms/', include('farms.urls', namespace="farms")),
    url(r'^users/', include('userprofile.urls', namespace="userprofile")),
    url(r'^announce/', include('announce.urls', namespace="announce")),
    url(r'^counties/', include('counties.urls', namespace="counties")),
    url(r'^memberorganizations/', include(
        'memberorgs.urls', namespace="memorgs")),
    url(r'^recipientsite/', include('recipientsite.urls', namespace="site")),
    url(r'^distribution/', include('distro.urls', namespace="distro")),
    url(r'^posts/', include('posts.urls', namespace="posts")),
    url(r'^initialize/', include('initialize.urls', namespace="initialize")),
    url(r'^api/', include('api.urls', namespace="api")),

    url(r'^omments/', include('django_comments.urls')),

    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),

    url(
        r'^accounts/register/$',
        MyRegistrationView.as_view(),
        name='registration_register'),
    # #url(r'^accounts/', include('userprofile.registration.MyBackEnd.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Examples:
    # url(r'^$', 'gleaning.views.home', name='home'),
    # url(r'^gleaning/', include('gleaning.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

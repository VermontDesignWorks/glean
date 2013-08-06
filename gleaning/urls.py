from django.conf.urls import patterns, include, url
from customreg import MyRegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import gleaning.settings as settings

urlpatterns = patterns('',
	url(r'^$', 'gleaning.views.home', name="home"),
	url(r'^glean/', include('gleanevent.urls', namespace="gleanevent")),
	url(r'^farms/', include('farms.urls', namespace="farms")),
	url(r'^users/', include('userprofile.urls', namespace="userprofile")),
	url(r'^announce/', include('announce.urls', namespace="announce")),
	url(r'^counties/', include('counties.urls', namespace="counties")),
	url(r'^testdata/', include('testdata.urls', namespace="testdata")),
	url(r'^memberorganizations/', include('memberorgs.urls', namespace="memorgs")),
	url(r'^recipientsite/', include('recipientsite.urls', namespace="site")),
	url(r'^distribution/', include('distro.urls', namespace="distro")),
	url(r'^posts/', include('posts.urls', namespace="posts")),
	url(r'^initialize/', include('initialize.urls', namespace="initialize")),

	url(r'^comments/', include('django.contrib.comments.urls')),

#	url(r'^accounts/register/$', register, {'backend': 'user_profile.regbackend.RegBackend','form_class': UserRegistrationForm}, name='registration_register'),
	#url(r'^accounts/', include('registration.backends.default.urls'), {'backend': 'userprofile.registration.MyBackEnd'}),
	url(r'^accounts/register/$',
                           MyRegistrationView.as_view(),
                           name='registration_register'),
	# #url(r'^accounts/', include('userprofile.registration.MyBackEnd.urls')),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^accounts/', include('registration.backends.default.urls', namespace="registration")),

	# Examples:
	# url(r'^$', 'gleaning.views.home', name='home'),
	# url(r'^gleaning/', include('gleaning.foo.urls')),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

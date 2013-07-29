from django.conf.urls import patterns, include, url
from registration import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

##registration imports
#from XXXXX import UserRegistrationForm


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

	url(r'^comments/', include('django.contrib.comments.urls')),

#	url(r'^accounts/register/$', register, {'backend': 'user_profile.regbackend.RegBackend','form_class': UserRegistrationForm}, name='registration_register'),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^accounts/', include('registration.backends.default.urls', namespace="registration")),

	# Examples:
	# url(r'^$', 'gleaning.views.home', name='home'),
	# url(r'^gleaning/', include('gleaning.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

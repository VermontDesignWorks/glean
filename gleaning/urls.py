from django.conf.urls import patterns, include, url
#from registration.views import register

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

	## registration backend
	#url(r'^accounts/register/$', register, {'backend': 'user_profile.regbackend.RegBackend','form_class': 'UserRegistrationForm'}, name='registration_register'),
	#url(r'^accounts/*', include('registration.backends.default.urls')),

	# Examples:
	# url(r'^$', 'gleaning.views.home', name='home'),
	# url(r'^gleaning/', include('gleaning.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
)

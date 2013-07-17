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
	url(r'^announce/', include('announce.urls', namespace="announce")),
	url(r'^counties/', include('counties.urls', namespace="counties")),
	url(r'^testdata/', include('testdata.urls', namespace="testdata")),
	url(r'^memberorganizations/', include('memberorgs.urls', namespace="memorgs")),
	url(r'^recipientsite/', include('recipientsite.urls', namespace="site")),
	url(r'^distribution/', include('distro.urls', namespace="distro")),

	## registration backend
	#(r'^admin/', include('admin.urls')),
	# url(r'^register/complete/$',
 #                           'registration/registration_complete.html',
 #                           name='registration_complete'),
	# (r'^/accounts/change-password/$', 'django.contrib.auth.views.password_change'), 
	# (r'^/accounts/password-changed/$', 'django.contrib.auth.views.password_change_done'),
	# (r'^/accounts/reset-password/$', 'django.contrib.auth.views.password_reset'),
	# (r'^/accounts/password-reset/$', 'django.contrib.auth.views.password_reset_done'),
	# (r'^/accounts/password-reset-confirm/$', 'django.contrib.auth.views.password_reset_confirm'),
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

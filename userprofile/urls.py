from django.conf.urls import patterns, url

from userprofile import views


urlpatterns = patterns('',
	url(r'^$', views.userHome, name='userhome'),
	url(r'^login/$', views.userLogin, name="userlogin"),
	url(r'^logout/$', views.userLogout, name="userlogout"),
	url(r'^registration/$', views.userReg, name='registration'),
	url(r'^userDetailEntry/$', views.userDetailEntry, name='userdetailentry'),
	url(r'^(?P<glean_id>\d+)/$', views.userProfile, name='userprofile'),
	url(r'^(?P<glean_id>\d+)/edit/$', views.editProfile, name='editprofile'),
)
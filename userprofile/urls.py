from django.conf.urls import patterns, url

from userprofile import views


urlpatterns = patterns('',
	url(r'^userDetailEntry/$', views.userDetailEntry, name='userdetailentry'),
	url(r'^edit/$', views.userEdit, name="useredit"),
	url(r'^lists/$', views.userLists, name="userlists"),
	url(r'^(?P<user_id>\d+)/$', views.userProfile, name='userprofile'),
)
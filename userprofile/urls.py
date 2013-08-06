from django.conf.urls import patterns, url

from userprofile import views


urlpatterns = patterns('',
	url(r'^userDetailEntry/$', views.userDetailEntry, name='userdetailentry'),
	url(r'^edit/$', views.selfEdit, name="selfedit"),
	url(r'^lists/$', views.userLists, name="userlists"),
	url(r'^download/$', views.download, name='download'),
	url(r'^new/$', views.newUser, name='newuser'),
	url(r'^(?P<user_id>\d+)/$', views.userProfile, name='userprofile'),
	url(r'^(?P<user_id>\d+)/edit/$', views.userEdit, name='useredit'),
	url(r'^(?P<user_id>\d+)/promote/$', views.userPromote, name='userpromote'),
	url(r'^change/email/$', views.emailEdit, name='emailedit'),
	
)
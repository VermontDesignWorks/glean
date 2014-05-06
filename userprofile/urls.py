from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required

from userprofile import views


urlpatterns = patterns(
    '',
    url(r'^userDetailEntry/$', views.userDetailEntry, name='userdetailentry'),
    url(r'^edit/$', views.ProfileUpdateView.as_view(), name="selfedit"),
    url(r'^lists/$', views.userLists, name="userlists"),
    url(r'^download/$', views.download, name='download'),
    url(r'^new/$', views.newUser, name='newuser'),
    url(r'^(?P<pk>\d+)/$',
        permission_required(
            'userprofile.auth'
        )(views.UserProfileDetailView.as_view()),
        name='userprofile'),
    url(r'^(?P<pk>\d+)/delete/$',
        permission_required(
            'userprofile.auth'
        )(views.UserProfileDelete.as_view()),
        name="delete"),
    url(r'^(?P<user_id>\d+)/edit/$', views.userEdit, name='useredit'),
    url(r'^(?P<user_id>\d+)/promote/$', views.userPromote, name='userpromote'),
    url(r'^change/email/$', views.emailEdit, name='emailedit'),
    url(r'^(?P<user_id>\d+)/reaccept/$', views.reaccept, name='reaccept'),
)

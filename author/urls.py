from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from author import views, viewsauth

urlpatterns = [

    # GET  /author/:username
    url(r'^(?P<username>[0-9a-zA-Z_]+)$', views.GetUserDetails.as_view(),
        name = 'user_details'),

    # GET /author/friends/:username
    url(r'^friends/(?P<username>[0-9a-zA-Z_]+)$', views.GetAuthorFriends.as_view(),
        name = 'user_friends'),

    # GET /author/followers/:username
    url(r'^followers/(?P<username>[0-9a-zA-Z_]+)$', views.GetAuthorFollowers.as_view(),
        name = 'user_followers'),

    # GET /author/friendrequests/:username
    url(r'^friendrequests/(?P<username>[0-9a-fA-Z_]+)$', views.GetAuthorFriendRequests.as_view(),
        name = 'user_friend_requests'),

    # POST /author/registration/
    url(r'^registration/$', viewsauth.AuthorRegistration,
        name = 'registration'),

    # POST /login
    url(r'^login/$', viewsauth.Login.as_view(), name='login'),

    # POST /logout
    url(r'^logout/$', viewsauth.Logout.as_view(), name='logout'),

   # GET /author/getid/:username
   # url(r'^getid/(?P<username>[0-9a-zA-Z]+)$', viewsauth.GetUserUUID,
   #     name = 'user_uuid'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

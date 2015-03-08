from django.conf.urls import url, include
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
    url(r'^friendrequests/(?P<username>[0-9a-zA-Z_]+)$', views.GetAuthorFriendRequests.as_view(),
        name = 'user_friend_requests'),

    # POST /author/registration/
    url(r'^registration/$', viewsauth.AuthorRegistration.as_view(),
        name = 'registration'),

    # GET /login
    url(r'^login/$', viewsauth.Login.as_view(), name='login'),

    # POST /logout
    url(r'^logout/$', viewsauth.Logout.as_view(), name='logout')
]

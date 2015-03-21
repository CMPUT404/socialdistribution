from django.conf.urls import url
import views, viewsauth

urlpatterns = [

    # GET /login
    url(r'^login/?$', viewsauth.Login.as_view(), name='login'),

    # POST /logout
    url(r'^logout/?$', viewsauth.Logout.as_view(), name='logout'),

    # GET POST /author/profile
    url(r'^profile/?$', viewsauth.AuthorProfile.as_view(), name='profile'),

    # GET /author/friends/:username
    url(r'^friends/(?P<id>[0-9a-zA-Z_]+)/?$', views.GetAuthorFriends.as_view(),
        name = 'user_friends'),

    # GET /author/followers/:username
    url(r'^followers/(?P<id>[0-9a-zA-Z_]+)/?$', views.GetAuthorFollowers.as_view(),
        name = 'user_followers'),

    # GET /author/friendrequests/:username
    url(r'^friendrequests/(?P<id>[0-9a-zA-Z_]+)/?$', views.GetAuthorFriendRequests.as_view(),
        name = 'user_friend_requests'),

    # POST /author/registration/
    url(r'^registration/?$', viewsauth.AuthorRegistration.as_view(),
        name = 'registration'),

    # GET /author/images/
    url(r'^images/(?P<id>.*)', views.Images.as_view(),
        name = 'images'),
]

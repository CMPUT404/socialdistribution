from django.conf.urls import url
import views, viewsauth

urlpatterns = [

    # GET /login
    url(r'^author/login/?$', viewsauth.Login.as_view(), name='login'),

    # POST /logout
    url(r'^author/logout/?$', viewsauth.Logout.as_view(), name='logout'),

    # GET POST /author/profile
    url(r'^author/profile/?$', viewsauth.AuthorProfile.as_view(), name='profile'),

    # GET /author/friends/:username
    # url(r'^friends/(?P<id>[0-9a-zA-Z_]+)/?$', views.GetAuthorFriends.as_view(),
    #     name = 'user_friends'),

    # POST /friends/:aid/:fid
    url(r'^friends/(?P<aid>[0-9a-zA-Z_]+)/(?P<fid>[0-9a-zA-Z_]+)/?$', views.GetFriends.as_view(),
        name = 'user_friends'),

    # GET/POST/DELETE /followers/:username
    url(r'^followers/(?P<id>[0-9a-zA-Z_]+)/?$', views.FollowersView.as_view(),
        name = 'user_followers'),

    # GET /friendrequests
    url(r'^friendrequest/?$', views.CreateFriendRequest.as_view(),
        name = 'author_friend_requests'),

    # POST /author/registration/
    url(r'^author/registration/?$', viewsauth.AuthorRegistration.as_view(),
        name = 'registration'),

    # GET /author/images/
    url(r'^images/(?P<id>.*)', views.Images.as_view(),
        name = 'images'),
]

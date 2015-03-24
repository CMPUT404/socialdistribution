from django.conf.urls import url
import views, viewsauth

urlpatterns = [

    # GET /login
    url(r'^author/login/?$', viewsauth.Login.as_view(), name='login'),

    # POST /logout
    url(r'^author/logout/?$', viewsauth.Logout.as_view(), name='logout'),

    # GET POST /author/profile
    url(r'^author/profile/?$', viewsauth.AuthorProfile.as_view(), name='profile'),

    # POST /friends/:aid/:fid
    url(r'^friends/(?P<aid>[0-9a-zA-Z_]+)/(?P<fid>[0-9a-zA-Z_]+)/?$', views.GetFriends.as_view(),
        name = 'user_friends'),

    # GET /friendrequests
    url(r'^friendrequest/?$', views.CreateFriendRequest.as_view(),
        name = 'author_friend_requests'),

    # POST /author/registration/
    url(r'^author/registration/?$', viewsauth.AuthorRegistration.as_view(),
        name = 'registration'),

    # GET /author/:path_prefix/images/:imageid
    url(r'^author/(?P<path_prefix>[a-zA-Z]+)/images/(?P<id>.*)', views.Images.as_view(),
        name = 'images'),
]

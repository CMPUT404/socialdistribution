from django.conf.urls import url
import views, viewsauth
import content_api.views as content_views

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

    # GET  /author/:id/posts
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/?$', content_views.GetPostsByAuthor.as_view()),

    # GET for single post /author/:id/posts/:postid
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/(?P<postid>[0-9a-zA-Z_]+)/?$', content_views.GetSinglePostByAuthor.as_view()),

    # Keep last
    # GET  /author/:id
    url(r'^(?P<id>[0-9a-zA-Z_]+)/?$', views.GetAuthorDetails.as_view(),
        name = 'author_details')
]

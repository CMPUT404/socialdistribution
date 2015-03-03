from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from author import views, viewsauth

urlpatterns = [

    # GET  /author/:uuid
    url(r'^author/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetUserDetails.as_view(),
        name = 'user_details'),

    # GET /author/friends/:uuid
    url(r'^author/friends/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetAuthorFriends.as_view(),
        name = 'user_friends'),

    # GET /author/followers/:uuid
    url(r'^author/followers/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetAuthorFollowers.as_view(),
        name = 'user_followers'),

    # GET /author/friendrequests/:uuid
    url(r'^author/friendrequests/(?P<uuid>[0-9a-fA-Z]{32}\Z)$', views.GetAuthorFriendRequests.as_view(),
        name = 'user_friend_requests'),

    # POST /author/registration/
    url(r'^author/registration/$', viewsauth.AuthorRegistration,
        name = 'registration'),

    # POST /login
    url(r'^login/$', viewsauth.Login.as_view(), name='login'),

]

urlpatterns = format_suffix_patterns(urlpatterns)

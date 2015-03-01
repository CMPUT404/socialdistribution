from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from author import views, viewsauth

urlpatterns = [

    # GET  /author/:uuid
    url(r'^author/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetUserDetails.as_view()),

    # GET /author/friends/:uuid
    url(r'^author/friends/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetAuthorFriends.as_view()),

    # GET /author/followers/:uuid
    url(r'^author/followers/(?P<uuid>[0-9a-zA-Z]{32}\Z)$', views.GetAuthorFollowers.as_view()),

    # GET /author/friendrequests/:uuid
    url(r'^author/friendrequests/(?P<uuid>[0-9a-fA-Z]{32}\Z)$', views.GetAuthorFriendRequests.as_view()),

    # Authentication URI
    url(r'^author/registration/$', viewsauth.AuthorRegistration),
]

urlpatterns = format_suffix_patterns(urlpatterns)

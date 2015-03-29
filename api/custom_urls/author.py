from django.conf.urls import url
from ..views import author, authentication, image
from ..views.image import AuthorImage

urlpatterns = [

    # GET /login
    url(r'^author/login/?$', authentication.Login.as_view(), name='login'),

    # POST /logout
    url(r'^author/logout/?$', authentication.Logout.as_view(), name='logout'),

    # GET POST /author/profile
    url(r'^author/profile/?$', authentication.AuthorProfile.as_view(), name='profile'),

    # POST friends/:fid
    url(r'^friends/(?P<fid>[0-9a-zA-Z_]+)/?$', author.FriendsWith.as_view(), name='check_friends'),

    # POST /friends/:aid/:fid
    url(r'^friends/(?P<aid>[0-9a-zA-Z_]+)/(?P<fid>[0-9a-zA-Z_]+)/?$', author.GetFriends.as_view(),
        name = 'user_friends'),

    # GET /friendrequests
    url(r'^friendrequest/?$',author.CreateFriendRequest.as_view(),
        name = 'author_friend_requests'),

    # POST /author/registration/
    url(r'^author/registration/?$', authentication.AuthorRegistration.as_view(),
        name = 'registration'),

    # GET /author/:id/image
    url(r'^author/(?P<aid>[a-zA-Z0-9]+)/image/?$', AuthorImage.as_view(),
        name = 'author_image'),

]

from django.conf.urls import url
from ..views.content import CreateComment, DeleteComment
from ..views.image import PostImage

urlpatterns = [
    # POST /post/:postid/comments
    url(r'^/(?P<postid>[0-9a-zA-Z]+)/comments/?$', CreateComment.as_view()),

    # DELETE /post/:id/comments/:commentid
    url(r'^/(?P<postid>[0-9a-zA-Z]+)/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', DeleteComment.as_view())
]

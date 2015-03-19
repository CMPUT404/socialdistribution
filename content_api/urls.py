from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [

    # GET  /author/:id/posts
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/?$', views.GetPostsByAuthor.as_view()),

    # GET for single post /author/:id/posts/:postid
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/(?P<postid>[0-9a-zA-Z_]+)/?$', views.GetSinglePostByAuthor.as_view()),



    # POST /author/posts/:postid/comments
    url(r'^posts/(?P<postid>[0-9a-zA-Z]+)/comments/?$', views.CreateComment.as_view()),

    # DELETE /author/posts/:postid
    url(r'^posts/(?P<postid>[0-9a-zA-Z]+)/?$', views.DeletePost.as_view()),

    # GET /post/:postid
    url(r'^/(?P<postid>[0-9a-zA-Z]+)/?$', views.GetSinglePost.as_view()),

    # GET /author/posts
    url(r'^posts/?$', views.GetTimeline.as_view()),

    # DELETE /author/posts/comments/:commentid
    url(r'^posts/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', views.DeleteComment.as_view()),

    # POST /post
    url(r'^$', views.CreatePost.as_view()),
]

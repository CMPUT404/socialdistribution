from django.conf.urls import url
from rest_framework import routers
import views

urlpatterns = [

    # GET  /author/:id/posts
    # url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/?$', views.GetPostsByAuthor.as_view()),

    # GET for single post /author/:id/posts/:postid
    # url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/(?P<postid>[0-9a-zA-Z_]+)/?$', views.GetSinglePostByAuthor.as_view()),

    # POST /post/:postid/comments
    url(r'^(?P<postid>[0-9a-zA-Z]+)/comments/?$', views.CreateComment.as_view()),

    # DELETE /author/posts/:postid
    # url(r'^posts/(?P<postid>[0-9a-zA-Z]+)/?$', views.DeletePost.as_view()),

    # GET /post/:postid
    # url(r'^/(?P<postid>[0-9a-zA-Z]+)/?$', views.GetSinglePost.as_view()),

    # DELETE /author/posts/comments/:commentid
    url(r'^?P(?P<postid>[0-9a-zA-Z]+)/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', views.DeleteComment.as_view())
]

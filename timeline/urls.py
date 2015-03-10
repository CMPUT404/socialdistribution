from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/:username/posts
    url(r'^(?P<username>[0-9a-zA-Z_]+)/posts/?$', views.GetPosts.as_view()),

    # GET for single post /author/:username/posts/:postid
    url(r'^(?P<username>[0-9a-zA-Z_]+)/posts/(?P<postid>[0-9a-zA-Z_]+)/?$', views.GetPosts.as_view()),

    # POST /author/post
    url(r'^post/?$', views.CreatePost.as_view()),

    # POST /author/posts/:postid/comments
    url(r'^posts/(?P<postid>[0-9a-zA-Z]+)/comments/?$', views.GetDeleteAddComments.as_view()),

    # DELETE /author/posts/comments/:commentid
    url(r'^posts/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', views.GetDeleteAddComments.as_view()),
]

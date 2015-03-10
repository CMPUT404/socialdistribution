from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/:id/posts
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/?$', views.GetPosts.as_view()),

    # GET for single post /author/:id/posts/:postid
    url(r'^(?P<id>[0-9a-zA-Z_]+)/posts/(?P<postid>[0-9a-zA-Z_]+)/?$', views.GetPosts.as_view()),

    # POST /author/post
    url(r'^post/?$', views.CreatePost.as_view()),

    # GET /author/timeline
    url(r'^timeline/?$', views.GetTimeline.as_view()),

    # POST /author/posts/:postid/comments
    url(r'^posts/(?P<postid>[0-9a-zA-Z]+)/comments/?$', views.GetDeleteAddComments.as_view()),

    # DELETE /author/posts/comments/:commentid
    url(r'^posts/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', views.GetDeleteAddComments.as_view()),
]

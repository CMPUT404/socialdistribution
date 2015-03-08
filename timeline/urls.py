from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/:username/posts
    url(r'^(?P<username>[0-9a-zA-Z_]+)/posts/?$', views.GetPosts.as_view()),

    # POST /author/post
    url(r'^post/?$', views.CreatePost.as_view()),
]

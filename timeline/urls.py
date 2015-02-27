from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/:uuid/posts
    url(r'^author/(?P<uuid>[0-9a-zA-Z]+)/posts$', views.GetPosts.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

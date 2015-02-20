from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from timeline import views

urlpatterns = [

    # GET  /author/posts/:uuid
    url(r'^author/posts/(?P<aid>[0-9]+)$', views.GetPosts.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)

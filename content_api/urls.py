from django.conf.urls import url
import views

urlpatterns = [
    # POST /post/:postid/comments
    url(r'^(?P<postid>[0-9a-zA-Z]+)/comments/?$', views.CreateComment.as_view()),

    # DELETE /post/:id/comments/:commentid
    url(r'^?(?P<postid>[0-9a-zA-Z]+)/comments/(?P<commentid>[0-9a-zA-Z]+)/?$', views.DeleteComment.as_view())
]

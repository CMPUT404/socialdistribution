from django.conf.urls import patterns, include, url
from django.contrib import admin
from author_api.views import AuthorViewSet
from content_api.views import PostViewSet, PublicPostViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'author', AuthorViewSet)
router.register(r'post', PostViewSet)
router.register(r'post', PublicPostViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/', include('author_api.urls')),
    # lets us access endpoints through /post or /author
    url(r'^post/', include('content_api.urls')),
    # url(r'^author/', include('content_api.urls')),
)

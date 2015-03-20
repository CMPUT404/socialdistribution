from django.conf.urls import patterns, include, url
from django.contrib import admin
from content_api.views import PostViewSet, AuthorPostViewSet, PublicPostsViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'author', AuthorPostViewSet)
router.register(r'post', PostViewSet)
router.register(r'posts', PublicPostsViewSet)

author_router = routers.NestedSimpleRouter(router, r'author', lookup='author',trailing_slash=False)
author_router.register(r'posts', AuthorPostViewSet)

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/', include('author_api.urls')),
    url(r'^post', include('content_api.urls')),
    url(r'^', include(router.urls)),
    url(r'^', include(author_router.urls))
)

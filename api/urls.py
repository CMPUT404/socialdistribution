from django.conf.urls import patterns, include, url
from django.contrib import admin
from views.content import PostViewSet, AuthorPostViewSet, PublicPostsViewSet
from rest_framework_nested import routers
from custom_urls import content as ContentUrls
from custom_urls import author as AuthorUrls
from views.author import FollowerViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'post', PostViewSet)
router.register(r'author', AuthorPostViewSet)
router.register(r'posts', PublicPostsViewSet)

author_router = routers.NestedSimpleRouter(router, r'author', lookup='author',trailing_slash=False)
author_router.register(r'posts', AuthorPostViewSet)
author_router.register(r'follow', FollowerViewSet)

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^post', include(ContentUrls)),
    url(r'^', include(AuthorUrls)),
    url(r'^', include(router.urls)),
    url(r'^', include(author_router.urls)),
)

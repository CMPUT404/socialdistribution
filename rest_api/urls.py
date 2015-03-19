from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^author/', include('author_api.urls')),
    # lets us access endpoints through /post or /author
    url(r'^post/?', include('content_api.urls')),
    # url(r'^author/', include('content_api.urls')),
)

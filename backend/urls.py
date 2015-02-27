from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'backend.views.home', name='home'), # Homepage for now

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('timeline.urls')),
    url(r'^', include('author.urls')),


)

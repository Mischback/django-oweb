# Django imports
from django.conf.urls import patterns, url

urlpatterns = patterns('oweb.views', 
    url(r'^$', 'home'),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='app_login'),
)

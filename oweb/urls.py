# Django imports
from django.conf.urls import patterns, url

urlpatterns = patterns('oweb.views',
    url(r'^$', 'home', name='home'),
)

urlpatterns += patterns('',
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'app_login.html'},
        name='app_login'),
)

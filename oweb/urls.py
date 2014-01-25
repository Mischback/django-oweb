# Django imports
from django.conf.urls import patterns, url

urlpatterns = patterns('oweb.views',
    url(r'^$', 'home', name='home'),
    url(r'^(?P<account_id>\d+)$', 'account_overview', name='account_overview'),

    url(r'^planet/(?P<planet_id>\d+)$', 'planet_overview', name='planet_overview'),
    url(r'^(?P<account_id>\d+)/planet-create$', 'planet_create', name='planet_create'),
)

urlpatterns += patterns('',
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'app_login.html'},
        name='app_login'),
)

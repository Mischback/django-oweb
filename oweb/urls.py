# Django imports
from django.conf.urls import patterns, url

urlpatterns = patterns('oweb.views',
    url(r'^$', 'home', name='home'),
    url(r'^update$', 'item_update', name='item_update'),

    url(r'^(?P<account_id>\d+)$',
        'account_overview', name='account_overview'),
    url(r'^(?P<account_id>\d+)/settings$',
        'account_settings', name='account_settings'),
    url(r'^(?P<account_id>\d+)/settings/commit$',
        'account_settings_commit', name='account_settings_commit'),
    url(r'^(?P<account_id>\d+)/research$',
        'account_research', name='account_research'),
    url(r'^(?P<account_id>\d+)/ships$',
        'account_ships', name='account_ships'),
    url(r'^(?P<account_id>\d+)/empire$',
        'account_empire', name='account_empire'),

    url(r'^planet/(?P<planet_id>\d+)$',
        'planet_overview', name='planet_overview'),
    url(r'^(?P<account_id>\d+)/planet/create$',
        'planet_create', name='planet_create'),
    url(r'^planet/(?P<planet_id>\d+)/settings$',
        'planet_settings', name='planet_settings'),
    url(r'^planet/(?P<planet_id>\d+)/settings/update$',
        'planet_settings_commit', name='planet_settings_update'),
    url(r'^planet/(?P<planet_id>\d+)/buildings$',
        'planet_buildings', name='planet_buildings'),
    url(r'^planet/(?P<planet_id>\d+)/defense$',
        'planet_defense', name='planet_defense'),
)

urlpatterns += patterns('',
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'oweb/login.html'},
        name='app_login'),
)

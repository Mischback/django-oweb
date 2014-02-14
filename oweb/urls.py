# Django imports
from django.conf.urls import patterns, url

urlpatterns = patterns('oweb.views',
    # basic.py
    url(r'^$', 'home', name='home'),

    # updates.py
    url(r'^update$', 'item_update', name='item_update'),
    url(r'^(?P<account_id>\d+)/settings/commit$',
        'account_settings_commit', name='account_settings_commit'),
    url(r'^planet/(?P<planet_id>\d+)/settings/update$',
        'planet_settings_commit', name='planet_settings_update'),
    url(r'^create$', 'create_account', name='create_account'),
    url(r'^(?P<account_id>\d+)/planet/create$',
        'planet_create', name='planet_create'),
    url(r'^delete/(?P<account_id>\d+)/(?P<planet_id>\d+)$',
        'planet_delete', name='planet_delete'),
    url(r'^delete/(?P<account_id>\d+)$',
        'account_delete', name='account_delete'),
    url(r'^planet/(?P<planet_id>\d+)/moon$',
        'moon_create', name='moon_create'),
    url(r'^moon/(?P<moon_id>\d+)/settings/commit$',
        'moon_settings_commit', name='moon_settings_commit'),
    url(r'^delete/moon/(?P<moon_id>\d+)$',
        'moon_delete', name='moon_delete'),

    # account.py
    url(r'^(?P<account_id>\d+)$',
        'account_overview', name='account_overview'),
    url(r'^(?P<account_id>\d+)/settings$',
        'account_settings', name='account_settings'),
    url(r'^(?P<account_id>\d+)/research$',
        'account_research', name='account_research'),
    url(r'^(?P<account_id>\d+)/ships$',
        'account_ships', name='account_ships'),
    url(r'^(?P<account_id>\d+)/empire$',
        'account_empire', name='account_empire'),

    # planet.py
    url(r'^planet/(?P<planet_id>\d+)$',
        'planet_overview', name='planet_overview'),
    url(r'^planet/(?P<planet_id>\d+)/settings$',
        'planet_settings', name='planet_settings'),
    url(r'^planet/(?P<planet_id>\d+)/buildings$',
        'planet_buildings', name='planet_buildings'),
    url(r'^planet/(?P<planet_id>\d+)/defense$',
        'planet_defense', name='planet_defense'),

    url(r'^moon/(?P<moon_id>\d+)$',
        'moon_overview', name='moon_overview'),
    url(r'^moon/(?P<moon_id>\d+)/settings$',
        'moon_settings', name='moon_settings'),
    url(r'^moon/(?P<moon_id>\d+)/buildings$',
        'moon_buildings', name='moon_buildings'),
    url(r'^moon/(?P<moon_id>\d+)/defense$',
        'moon_defense', name='moon_defense'),

    # tools.py
    url(r'^tools/(?P<account_id>\d+)/energy$',
        'tools_energy', name="tools_energy"),
    url(r'^tools/(?P<account_id>\d+)/energy/(?P<energy_level>\d+)/(?P<fusion_level>\d+)$',
        'tools_energy', name="tools_energy_draft"),
)

urlpatterns += patterns('',
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'oweb/login.html'},
        name='app_login'),
    url(r'^logout/$',
        'django.contrib.auth.views.logout', {'next_page': '/'},
        name='app_logout')
)

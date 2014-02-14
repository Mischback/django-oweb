# Python imports
from datetime import datetime
import hashlib
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
# app imports
from oweb.models import Account, Building, Civil212, Defense, Planet, Research113, Research122, Moon
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue
from oweb.libs.points import get_planet_points


def planet_overview(req, planet_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planet = Planet.objects.select_related('account').get(id=planet_id)
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    try:
        moon = Moon.objects.get(planet=planet.id)
    except Moon.DoesNotExist:
        moon = None
    planets = Planet.objects.filter(account_id=planet.account.id)
    plasma = get_object_or_404(Research122, account=planet.account.id)
    energy = get_object_or_404(Research113, account=planet.account.id)
    buildings = get_list_or_404(Building, astro_object=planet_id)

    planet_fields = 0
    for b in buildings:
        planet_fields += b.level

    production = get_planet_production(planet, planet.account.speed)
    queue = get_planet_queue(planet)
    points = get_planet_points(planet)

    return render(req, 'oweb/planet_overview.html',
        {
            'account': planet.account,
            'planet': planet,
            'moon': moon,
            'planets': planets,
            'planet_fields': planet_fields,
            'production': production,
            'queue': queue,
            'points': points,
        }
    )


def planet_settings(req, planet_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planet = Planet.objects.select_related('account').get(id=planet_id)
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    try:
        moon = Moon.objects.get(planet=planet.id)
    except Moon.DoesNotExist:
        moon = None
    planets = Planet.objects.filter(account_id=planet.account.id)

    return render(req, 'oweb/planet_settings.html',
        {
            'account': planet.account,
            'planet': planet,
            'moon': moon,
            'planets': planets,
            'planets_url': 'oweb:planet_settings',
        }
    )


def planet_buildings(req, planet_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        buildings = Building.objects.select_related('astro_object', 'astro_object__account').filter(astro_object=planet_id)
        planet = buildings.first().astro_object.as_real_class()
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    try:
        moon = Moon.objects.get(planet=planet.id)
    except Moon.DoesNotExist:
        moon = None
    planets = Planet.objects.filter(account_id=planet.account.id)
    solarsat = get_object_or_404(Civil212, astro_object=planet_id)

    return render(req, 'oweb/planet_buildings.html',
        {
            'account': planet.account,
            'planet': planet,
            'moon': moon,
            'planets': planets,
            'planets_url': 'oweb:planet_buildings',
            'buildings': buildings,
            'solarsat': solarsat,
            'True': True,
            'False': False,
        }
    )


def planet_defense(req, planet_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        defense = Defense.objects.select_related('astro_object', 'astro_object__account').filter(astro_object=planet_id)
        planet = defense.first().astro_object.as_real_class()
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    try:
        moon = Moon.objects.get(planet=planet.id)
    except Moon.DoesNotExist:
        moon = None
    planets = Planet.objects.filter(account_id=planet.account.id)

    return render(req, 'oweb/planet_defense.html',
        {
            'account': planet.account,
            'planet': planet,
            'moon': moon,
            'planets': planets,
            'planets_url': 'oweb:planet_defense',
            'defense': defense,
        }
    )


def moon_overview(req, moon_id):
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        moon = Moon.objects.select_related('planet','planet__account').get(id=moon_id)
    except Moon.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=moon.planet.account.id)

    return render(req, 'oweb/moon_overview.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'planets': planets,
        }
    )


def moon_buildings(req, moon_id):
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        buildings = Building.objects.select_related('astro_object', 'astro_object__planet').filter(astro_object=moon_id)
        moon = buildings.first().astro_object.as_real_class()
    except Moon.DoesNotExist:
        raise Http404
    except AttributeError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=moon.planet.account.id)
    solarsat = get_object_or_404(Civil212, astro_object=moon_id)

    return render(req, 'oweb/moon_buildings.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'planets': planets,
            'buildings': buildings,
            'solarsat': solarsat,
            'True': True,
            'False': False,
        }
    )


def moon_defense(req, moon_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        defense = Defense.objects.select_related('astro_object', 'astro_object__planet').filter(astro_object=moon_id)
        moon = defense.first().astro_object.as_real_class()
    except Moon.DoesNotExist:
        raise Http404
    except AttributeError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=moon.planet.account.id)

    return render(req, 'oweb/moon_defense.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'planets': planets,
            'defense': defense,
        }
    )


def moon_settings(req, moon_id):
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        moon = Moon.objects.select_related('planet','planet__account').get(id=moon_id)
    except Moon.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=moon.planet.account.id)

    return render(req, 'oweb/moon_settings.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'planets': planets,
        }
    )

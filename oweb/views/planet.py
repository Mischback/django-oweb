"""Contains all planet related views"""
# Python imports
from datetime import datetime
import hashlib
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
# app imports
from oweb.exceptions import OWebDoesNotExist, OWebAccountAccessViolation
from oweb.models import Account, Building, Civil212, Defense, Planet, Research113, Research122, Moon, Station41
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue
from oweb.libs.points import get_planet_points
from oweb.libs.shortcuts import get_list_or_404, get_object_or_404


def planet_overview(req, planet_id):
    """Provides the planet overview"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planet = Planet.objects.select_related('account').get(id=planet_id)
    except Planet.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

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
    """Provides the planet settings"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planet = Planet.objects.select_related('account').get(id=planet_id)
    except Planet.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

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


def planet_settings_commit(req, planet_id):
    """Commits the planet's settings"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planet = Planet.objects.select_related('account').get(id=planet_id)
    except Planet.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

    try:
        planet.name = req.POST['planet_name']
        planet.coord = req.POST['planet_coord']
        planet.max_temp = req.POST['planet_max_temp']
        planet.save()
    except KeyError:
        raise OWebParameterMissingException

    return redirect(reverse('oweb:planet_settings', args=[planet.id]))


def planet_buildings(req, planet_id):
    """Provides the planet buildings"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        buildings = Building.objects.select_related('astro_object', 'astro_object__account').filter(astro_object=planet_id)
        planet = buildings.first().astro_object.as_real_class()
    except Building.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

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
    """Provides the planet defense"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        defense = Defense.objects.select_related('astro_object', 'astro_object__account').filter(astro_object=planet_id)
        planet = defense.first().astro_object.as_real_class()
    except Defense.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

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


def planet_create(req, account_id):
    """Creates a :py:class:`Planet`"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    account = get_object_or_404(Account, pk=account_id)

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    planet = Planet.objects.create(account=account, name='Colony')

    return HttpResponseRedirect(reverse('oweb:planet_settings', args=[planet.id]))


def planet_delete(req, account_id, planet_id):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    planet = Planet.objects.select_related('account').get(pk=planet_id)

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

    if 'confirm' == req.POST.get('confirm_planet_deletion'):
        planet.delete()
        return redirect(reverse('oweb:account_overview', args=account_id))

    return render(req, 'oweb/planet_delete.html',
        {
            'account': planet.account,
            'planet_del': planet,
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
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

    planets = Planet.objects.filter(account_id=moon.planet.account.id)

    buildings = Building.objects.filter(astro_object=moon_id)
    moon_fields = 0
    for b in buildings:
        moon_fields += b.level

    base = Station41.objects.get(astro_object=moon_id)
    moon_fields = (moon_fields, base.level * 3 + 1)

    return render(req, 'oweb/moon_overview.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'moon_fields': moon_fields,
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
        raise OWebDoesNotExist
    except AttributeError:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

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
        raise OWebDoesNotExist
    except AttributeError:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

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
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

    planets = Planet.objects.filter(account_id=moon.planet.account.id)

    return render(req, 'oweb/moon_settings.html',
        {
            'account': moon.planet.account,
            'planet': moon.planet,
            'moon': moon,
            'planets': planets,
        }
    )


def moon_create(req, planet_id):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    planet = get_object_or_404(Planet, pk=planet_id)

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise OWebAccountAccessViolation

    try:
        moon = Moon.objects.get(planet=planet)
    except Moon.DoesNotExist:
        tmp_name = hashlib.md5(str(datetime.now))
        Moon.objects.create(planet=planet, name=tmp_name, coord=planet.coord)

        moon = get_object_or_404(Moon, name=tmp_name)
        moon.name = 'Moon'
        moon.save()

    return HttpResponseRedirect(reverse('oweb:moon_settings', args=(moon.id,)))


def moon_settings_commit(req, moon_id):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        moon = Moon.objects.select_related('planet', 'planet__account').get(id=moon_id)
    except Moon.DoesNotExist:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

    try:
        moon.name = req.POST['moon_name']
        moon.save()
    except KeyError:
        raise OWebParameterMissingException

    return HttpResponseRedirect(reverse('oweb:moon_settings', args=[moon.id]))


def moon_delete(req, moon_id):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    try:
        moon = Moon.objects.select_related('planet', 'planet__account').get(id=moon_id)
    except Moon.DoesNotExist:
        raise OWebDoesNotExist

    planet = moon.planet

    # checks, if this account belongs to the authenticated user
    if not req.user.id == moon.planet.account.owner_id:
        raise OWebAccountAccessViolation

    if 'confirm' == req.POST.get('confirm_moon_deletion'):
        moon.delete()
        return redirect(reverse('oweb:planet_overview', args=(planet.id,)))

    return render(req, 'oweb/moon_delete.html',
        {
            'moon': moon
        }
    )

# Python imports
from datetime import datetime
import hashlib
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
# app imports
from oweb.models import Account, Building, Civil212, Defense, Planet, Research113, Research122
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue


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

    planets = Planet.objects.filter(account_id=planet.account.id)
    plasma = get_object_or_404(Research122, account=planet.account.id)
    energy = get_object_or_404(Research113, account=planet.account.id)
    buildings = get_list_or_404(Building, planet=planet_id)

    planet_fields = 0
    for b in buildings:
        planet_fields += b.level

    production = get_planet_production(planet, planet.account.speed)
    queue = get_planet_queue(planet)

    return render(req, 'oweb/planet_overview.html',
        {
            'account': planet.account,
            'planet': planet,
            'planets': planets,
            'planet_fields': planet_fields,
            'production': production,
            'queue': queue,
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

    planets = Planet.objects.filter(account_id=planet.account.id)

    return render(req, 'oweb/planet_settings.html',
        {
            'account': planet.account,
            'planet': planet,
            'planets': planets,
        }
    )


def planet_settings_commit(req, planet_id):
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

    planet.name = req.POST['planet_name']
    planet.coord = req.POST['planet_coord']
    planet.min_temp = req.POST['planet_min_temp']
    planet.save()

    return HttpResponseRedirect(reverse('oweb:planet_settings', args=(planet_id,)))


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
        building_list = Building.objects.select_related('planet', 'planet__account').filter(planet=planet_id)
        planet = building_list.first().planet
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=planet.account.id)
    s = get_object_or_404(Civil212, planet=planet_id)
    solarsat = {'name': s.name, 'level': s.count, 'id': s.id}

    buildings = []
    for b in building_list:
        buildings.append({'name': b.name, 'level': b.level, 'id': b.id})

    return render(req, 'oweb/planet_buildings.html',
        {
            'account': planet.account,
            'planet': planet,
            'planets': planets,
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
        defense_list = Defense.objects.select_related('planet', 'planet__account').filter(planet=planet_id)
        planet = defense_list.first().planet
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == planet.account.owner_id:
        raise Http404

    planets = Planet.objects.filter(account_id=planet.account.id)
    defense = get_list_or_404(Defense, planet=planet_id)

    return render(req, 'oweb/planet_defense.html',
        {
            'account': planet.account,
            'planet': planet,
            'planets': planets,
            'defense': defense,
        }
    )


def planet_create(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    account = get_object_or_404(Account, pk=account_id)

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    tmp_name = hashlib.md5(str(datetime.now))
    Planet.objects.create(account=account, name=tmp_name)

    planet = get_object_or_404(Planet, name=tmp_name)
    planet.name = 'Colony'
    planet.save()

    return HttpResponseRedirect(reverse('oweb:planet_settings', args=(planet.id,)))

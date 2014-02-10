# Python imports
from itertools import chain, izip_longest
# Django imports
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
# app imports
from oweb.models import Account, Building, Civil212, Defense, Planet, Research, Ship
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue, get_plasma_queue
from oweb.libs.points import get_planet_points, get_ship_points, get_research_points

def account_overview(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        planets = Planet.objects.select_related('account').filter(account_id=account_id)
        account = planets[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    # production
    production = []
    # queue
    queue = []
    # points
    total_points = 0
    production_points = 0
    other_points = 0
    defense_points = 0
    research_points = get_research_points(account)
    ship_points = get_ship_points(account)
    planet_points = []

    for p in planets:
        # production
        production.append(get_planet_production(p, account.speed))
        # queue
        queue += get_planet_queue(p)[:5]
        # points
        this_planet_points = get_planet_points(p)
        production_points += this_planet_points[1]
        other_points += this_planet_points[2]
        defense_points += this_planet_points[3]
        planet_points.append((this_planet_points, p))

    # production
    production = tuple(sum(x) for x in zip(*production))
    # queue
    queue += get_plasma_queue(account, production=production)
    queue.sort()
    queue = queue[:20]
    # points
    total_points = production_points + other_points + defense_points + research_points + ship_points[0]
    points = {}
    points['total'] = total_points
    try:
        points['production'] = (production_points, production_points / float(total_points) * 100)
    except ZeroDivisionError:
        points['production'] = (production_points, 0)
    try:
        points['other'] = (other_points, other_points / float(total_points) * 100)
    except ZeroDivisionError:
        points['other'] = (other_points, 0)
    try:
        points['defense'] = (defense_points, defense_points / float(total_points) * 100)
    except ZeroDivisionError:
        points['defense'] = (defense_points, 0)
    try:
        points['research'] = (research_points, research_points / float(total_points) * 100)
    except ZeroDivisionError:
        points['research'] = (research_points, 0)
    try:
        points['ships'] = (ship_points[0], ship_points[0] / float(total_points) * 100)
    except ZeroDivisionError:
        points['ships'] = (ship_points[0], 0)

    total_planet_points = []
    planet_points.sort(reverse=True)
    for p in planet_points:
        try:
            total_planet_points.append((p[1], p[0], p[0][0] / float(total_points) * 100))
        except ZeroDivisionError:
            total_planet_points.append((p[1], p[0], 0))

    points['planets'] = total_planet_points

    points['ogame'] = (
        production_points + other_points + defense_points + (ship_points[1] / 2),
        ship_points[2] + defense_points + (ship_points[1] / 2),
        research_points
    )

    return render(req, 'oweb/account_overview.html', 
        {
            'account': account,
            'planets': planets,
            'production': production,
            'queue': queue,
            'points': points,
        }
    )


def account_empire(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        planets = Planet.objects.select_related('account').filter(account_id=account_id)
        account = planets.first().account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    return render(req, 'oweb/account_empire.html', 
        {
            'account': account,
            'planets': planets,
        }
    )


def account_settings(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        planets = Planet.objects.select_related('account').filter(account_id=account_id)
        account = planets[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    return render(req, 'oweb/account_settings.html', 
        {
            'account': account,
            'planets': planets,
        }
    )


def account_research(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        research = Research.objects.select_related('account').filter(account=account_id)
        account = research[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    planets = get_list_or_404(Planet, account=account_id)

    return render(req, 'oweb/account_research.html', 
        {
            'account': account,
            'planets': planets,
            'research': research,
        }
    )


def account_ships(req, account_id):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        planets = Planet.objects.select_related('account').filter(account_id=account_id)
        account = planets[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    sat_id = ContentType.objects.get(model='civil212').id

    ships = Ship.objects.filter(account_id=account_id).exclude(content_type_id=sat_id)

    return render(req, 'oweb/account_ships.html', 
        {
            'account': account,
            'planets': planets,
            'ships': ships,
        }
    )

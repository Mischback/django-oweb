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

    production = []
    queue = []
    for p in planets:
        production.append(get_planet_production(p, account.speed))
        queue += get_planet_queue(p)[:5]

    production = tuple(sum(x) for x in zip(*production))
    queue += get_plasma_queue(account, production=production)
    queue.sort()
    queue = queue[:20]

    return render(req, 'oweb/account_overview.html', 
        {
            'account': account,
            'planets': planets,
            'production': production,
            'queue': queue,
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
        account = planets[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    # build a list of planet ids
    planet_ids = planets.values_list('id', flat=True)

    # fetch buildings and defense
    buildings = Building.objects.filter(planet_id__in=planet_ids)
    defense = Defense.objects.filter(planet_id__in=planet_ids)
    sats = Civil212.objects.filter(planet_id__in=planet_ids)

    meta_list = []
    building_list = []
    defense_list = []

    m =['Name', 'Coords', 'Temperature']
    meta_list.append(izip_longest([], m, fillvalue='plain'))
    b = buildings.filter(planet_id=planets[0].id).values_list('name', flat=True)
    s = sats.filter(planet_id=planets[0].id).values_list('name', flat=True)
    building_list.append(izip_longest([], chain(b, s), fillvalue='plain'))
    d = defense.filter(planet_id=planets[0].id).values_list('name', flat=True)
    defense_list.append(izip_longest([], d, fillvalue='plain'))
    for p in planets:
        # buildings
        b = buildings.filter(planet_id=p.id)
        s = sats.filter(planet_id=p.id)
        this_buildings = izip_longest([], b, fillvalue='building')
        this_buildings = chain(this_buildings, izip_longest([], s, fillvalue='ship'))
        building_list.append(this_buildings)

        # defense
        d = defense.filter(planet_id=p.id)
        this_def = izip_longest([], d, fillvalue='defense')
        defense_list.append(this_def)

        # planet meta information
        m = [p.name, p.coord, p.min_temp]
        this_meta = izip_longest([], m, fillvalue='plain')
        meta_list.append(this_meta)

    empire = [
        ['Meta', zip(*meta_list)],
        ['Buildings', zip(*building_list)],
        ['Defense', zip(*defense_list)],
    ]

    return render(req, 'oweb/account_empire.html', 
        {
            'account': account,
            'planets': planets,
            'empire': empire,
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

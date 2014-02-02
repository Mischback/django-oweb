# Django imports
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
# app imports
from oweb.models import Account, Building, Civil212, Defense, Planet, Research, Ship
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue, get_plasma_queue

def home(req):
    """
    @brief  Overview of all accounts of a user
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # get all accounts of this user
    accounts = get_list_or_404(Account, owner_id=req.user.id)
    # render the template
    return render(req, 'oweb/home.html', 
        {'accounts': accounts}
    )


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

    meta_list = []
    meta_list.append(['Name', 'Coords', 'Temperature'])
    building_list = []
    building_list.append(buildings.filter(planet_id=planets[0].id).values_list('name', flat=True))
    defense_list = []
    defense_list.append(defense.filter(planet_id=planets[0].id).values_list('name', flat=True))
    for p in planets:
        # buildings
        this_buildings = buildings.filter(planet_id=p.id).values_list('level', flat=True)
        building_list.append(this_buildings)
        # defense
        this_def = defense.filter(planet_id=p.id).values_list('count', flat=True)
        defense_list.append(this_def)

        # planet meta information
        meta_list.append([p.name, p.coord, p.min_temp])

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


def account_settings_commit(req, account_id):
    """
    """
    acc = get_object_or_404(Account, pk=account_id)

    acc.username = req.POST['account_username']
    acc.universe = req.POST['account_universe']
    acc.speed = req.POST['account_speed']
    acc.trade_metal = req.POST['account_trade_metal']
    acc.trade_crystal = req.POST['account_trade_crystal']
    acc.trade_deut = req.POST['account_trade_deut']
    acc.save()

    return HttpResponseRedirect(reverse('oweb:account_settings',
        args=(acc.id,)))


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
        res = Research.objects.select_related('account').filter(account=account_id)
        account = res[0].account
    except Planet.DoesNotExist:
        raise Http404
    except IndexError:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    planets = get_list_or_404(Planet, account=account_id)

    research = []
    for r in res:
        research.append({'name': r.name, 'level': r.level, 'id': r.id})

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

    sl = get_list_or_404(Ship, account=account_id)
    ships = []
    for s in sl:
        # exclude SolarSats
        if not s.content_type_id == sat_id:
            ships.append({'name': s.name, 'level': s.count, 'id': s.id})

    return render(req, 'oweb/account_ships.html', 
        {
            'account': account,
            'planets': planets,
            'ships': ships,
        }
    )

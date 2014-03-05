"""Contains all account related views"""
# Python imports
from itertools import chain, izip_longest, repeat
# Django imports
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
# app imports
from oweb.exceptions import OWebDoesNotExist, OWebAccountAccessViolation
from oweb.models import Account, Building, Civil212, Defense, Planet, Research, Ship, Moon
from oweb.libs.production import get_planet_production
from oweb.libs.queue import get_planet_queue, get_plasma_queue
from oweb.libs.points import get_planet_points, get_ship_points, get_research_points
from oweb.libs.shortcuts import get_object_or_404, get_list_or_404


def account_overview(req, account_id):
    """Provides the account overview"""
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
        raise OWebDoesNotExist
    except AttributeError:
        return redirect(reverse('oweb:account_delete', args=account_id))

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    # production
    production = []
    # queue
    queue = []
    # points
    total_points = 0
    production_points = 0
    other_points = 0
    defense_points = 0
    moon_points = 0
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
        defense_points += this_planet_points[6]
        moon_points += this_planet_points[5]
        planet_points.append((this_planet_points, p))

    # production
    production = tuple(sum(x) for x in zip(*production))
    # queue
    queue += get_plasma_queue(account, production=production)
    queue.sort()
    queue = queue[:20]
    # points
    total_points = production_points + other_points + defense_points + moon_points + research_points + ship_points[0]
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
        points['moons'] = (moon_points, moon_points / float(total_points) * 100)
    except ZeroDivisionError:
        points['moons'] = (moon_points, 0)
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
    """Provides the empire view"""
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
        raise OWebDoesNotExist
    except AttributeError:
        return redirect(reverse('oweb:account_delete', args=account_id))

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    tmp_meta = []
    tmp_buildings = []
    tmp_defense = []
    tmp_moon = []
    tmp_defense_points = []
    tmp_building_points = []
    moon_list = None
    for p in planets:
        tmp_points = get_planet_points(p)
        tmp_building_points.append(('plain', tmp_points[1] + tmp_points[2]))
        tmp_defense_points.append(('plain', tmp_points[3]))

        tmp_planet = []
        tmp_planet.append(('planet', p.id, p.name))
        tmp_planet.append(('coord', p.coord))
        tmp_planet.append(('temp', p.max_temp))
        tmp_planet.append(('points', tmp_points[0]))
        tmp_meta.append(tmp_planet)

        b_list = list(izip_longest(
            [],
            get_list_or_404(Building, astro_object=p),
            fillvalue='building'))
        b_list.append(('ship', get_object_or_404(Civil212, astro_object=p)))
        tmp_buildings.append(b_list)

        d_list = list(izip_longest(
            [],
            get_list_or_404(Defense, astro_object=p),
            fillvalue='defense'
        ))
        tmp_defense.append(d_list)

        try:
            moon = Moon.objects.get(planet=p)
            m_b_list = list(izip_longest(
                [],
                get_list_or_404(Building, astro_object=moon),
                fillvalue='moon_building'))
            m_d_list = list(izip_longest(
                [],
                get_list_or_404(Defense, astro_object=moon),
                fillvalue='moon_defense'))
            moon_list = m_b_list + m_d_list
            tmp_moon.append(moon_list)
        except Moon.DoesNotExist:
            tmp_moon.append([])

    tmp_meta.insert(0, [
        ('caption', 'Planet'),
        ('caption', 'Coordinates'),
        ('caption', 'Temperature'),
        ('caption', 'Points')
    ])
    tmp_meta = zip(*tmp_meta)

    tmp_buildings.insert(0, [('caption', i[1].name) for i in b_list])
    tmp_buildings = zip(*tmp_buildings)

    tmp_defense.insert(0, [('caption', i[1].name) for i in d_list])
    tmp_defense = zip(*tmp_defense)

    if moon_list:
        tmp_moon2 = tmp_moon
        tmp_moon = []
        moon_len = len(moon_list)
        for i in tmp_moon2:
            if len(i) < moon_len:
                tmp_moon.append(list(repeat(('no_moon', 0), moon_len)))
            else:
                tmp_moon.append(i)

        tmp_moon.insert(0, [('caption', i[1].name) for i in moon_list])
        tmp_moon = zip(*tmp_moon)


    empire = [
        ('Meta', tmp_meta),
        ('Buildings', tmp_buildings),
        ('Defense', tmp_defense),
        ('Moon', tmp_moon),
    ]

    return render(req, 'oweb/account_empire.html',
                  {
                      'account': account,
                      'planets': planets,
                      'empire': empire,
                  }
    )


def account_settings(req, account_id):
    """Provides the account settings"""
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
        raise OWebDoesNotExist
    except AttributeError:
        return redirect(reverse('oweb:account_delete', args=account_id))

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    return render(req, 'oweb/account_settings.html',
                  {
                      'account': account,
                      'planets': planets,
                  }
    )


def account_settings_commit(req, account_id):
    """Commits the account's settings"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    acc = get_object_or_404(Account, pk=account_id)

    # check, if the objects account is actually owned by the current user
    if not req.user.id == acc.owner_id:
        raise OWebAccountAccessViolation

    try:
        acc.username = req.POST['account_username']
        acc.universe = req.POST['account_universe']
        acc.speed = req.POST['account_speed']
        acc.trade_metal = req.POST['account_trade_metal']
        acc.trade_crystal = req.POST['account_trade_crystal']
        acc.trade_deut = req.POST['account_trade_deut']
        acc.save()
    except KeyError:
        raise OWebParameterMissingException
    except ValueError:
        raise OWebIllegalParameterException

    return redirect(reverse('oweb:account_settings', args=[acc.id]))


def account_research(req, account_id):
    """Provides the research overview"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the list of planets
    try:
        research = Research.objects.select_related('account').filter(account=account_id)
        account = research.first().account
    except Planet.DoesNotExist:
        raise OWebDoesNotExist
    except AttributeError:
        return redirect(reverse('oweb:account_delete', args=account_id))

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    planets = get_list_or_404(Planet, account=account_id)

    return render(req, 'oweb/account_research.html',
                  {
                      'account': account,
                      'planets': planets,
                      'research': research,
                  }
    )


def account_ships(req, account_id):
    """Provides the ship overview"""
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
        raise OWebDoesNotExist
    except AttributeError:
        return redirect(reverse('oweb:account_delete', args=account_id))

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    sat_id = ContentType.objects.get(model='civil212').id

    ships = Ship.objects.filter(account_id=account_id).exclude(content_type_id=sat_id)

    return render(req, 'oweb/account_ships.html',
                  {
                      'account': account,
                      'planets': planets,
                      'ships': ships,
                  }
    )


def account_create(req):
    """Creates an :py:class:`Account`"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    acc = Account()
    acc.owner = req.user
    acc.save()

    return redirect(reverse('oweb:account_settings', args=[acc.id]))


def account_delete(req, account_id):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    account = get_object_or_404(Account, pk=account_id)

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    if 'confirm' == req.POST.get('confirm_account_deletion'):
        account.delete()
        return redirect(reverse('oweb:home'))

    return render(req, 'oweb/account_delete.html',
        {
            'account': account,
        }
    )

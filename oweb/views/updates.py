"""Contains all views, that actually alters the database"""
# Python imports
from datetime import datetime
import hashlib
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
# app imports
from oweb.exceptions import OWebDoesNotExist, OWebAccountAccessViolation, OWebParameterMissingException, OWebIllegalParameterException
from oweb.models import Account, Building, Defense, Planet, Research, Ship, Moon
from oweb.libs.shortcuts import get_object_or_404


def item_update(req):
    """Generic function to update items

    Items are :py:class:`Building`, :py:class:`Research`, :py:class:`Ship`
    and :py:class:`Defense`"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    try:
        item_type = req.POST['item_type']
        item_id = req.POST['item_id']
        item_level = req.POST['item_level']
    except KeyError:
        raise OWebParameterMissingException

    if 'research' == item_type:
        obj = Research.objects.get(pk=item_id)
        account = obj.account
    elif 'ship' == item_type:
        obj = Ship.objects.get(pk=item_id)
        account = obj.account
    elif 'building' == item_type:
        obj = Building.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    elif 'moon_building' == item_type:
        obj = Building.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().planet.account
    elif 'defense' == item_type:
        obj = Defense.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    elif 'moon_defense' == item_type:
        obj = Defense.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().planet.account
    else:
        raise OWebIllegalParameterException

    # check, if the objects account is actually owned by the current user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    if not int(item_level) < 0:
        if isinstance(obj, Ship) or isinstance(obj, Defense):
            obj.count = item_level
        else:
            obj.level = item_level
        obj.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


def create_account(req):
    """Creates an :py:class:`Account`"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    acc = Account()
    acc.owner = req.user
    acc.save()

    return redirect(reverse('oweb:account_settings', args=[acc.id]),
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

    planet.name = req.POST['planet_name']
    planet.coord = req.POST['planet_coord']
    planet.max_temp = req.POST['planet_max_temp']
    planet.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


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

    tmp_name = hashlib.md5(str(datetime.now))
    Planet.objects.create(account=account, name=tmp_name)

    planet = get_object_or_404(Planet, name=tmp_name)
    planet.name = 'Colony'
    planet.save()

    return HttpResponseRedirect(reverse('oweb:planet_settings', args=(planet.id,)))


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

    moon.name = req.POST['moon_name']
    moon.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


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

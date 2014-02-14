# Python imports
from datetime import datetime
import hashlib
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
# app imports
from oweb.models import Account, Building, Defense, Planet, Research, Ship, Moon

def item_update(req):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    try:
        item_type = req.POST['item_type']
        item_id = req.POST['item_id']
        item_level = req.POST['item_level']
    except:
        raise Http404

    if 'research' == item_type:
        obj = Research.objects.select_related('account').get(pk=item_id)
        account = obj.account
    elif 'ship' == item_type:
        obj = Ship.objects.select_related('account').get(pk=item_id)
        account = obj.account
    elif 'building' == item_type:
        obj = Building.objects.select_related('planet__account').get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    elif 'defense' == item_type:
        obj = Defense.objects.select_related('planet__account').get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    else:
        raise Http404

    # check, if the objects account is actually owned by the current user
    if not req.user.id == account.owner_id:
        raise Http404

    if not int(item_level) < 0:
        if isinstance(obj, Ship) or isinstance(obj, Defense):
            obj.count = item_level
        else:
            obj.level = item_level
        obj.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


def create_account(req):
    """todo Documentation still missing!"""
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
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    acc = get_object_or_404(Account, pk=account_id)

    acc.username = req.POST['account_username']
    acc.universe = req.POST['account_universe']
    acc.speed = req.POST['account_speed']
    acc.trade_metal = req.POST['account_trade_metal']
    acc.trade_crystal = req.POST['account_trade_crystal']
    acc.trade_deut = req.POST['account_trade_deut']
    acc.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


def planet_settings_commit(req, planet_id):
    """todo Documentation still missing!"""
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

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


def planet_create(req, account_id):
    """todo Documentation still missing!"""
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
        raise Http404

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
        raise Http404

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
        raise Http404

    tmp_name = hashlib.md5(str(datetime.now))
    Moon.objects.create(planet=planet, name=tmp_name, coord=planet.coord)

    moon = get_object_or_404(Moon, name=tmp_name)
    moon.name = 'Moon'
    moon.save()

    return HttpResponseRedirect(reverse('oweb:moon_settings', args=(moon.id,)))

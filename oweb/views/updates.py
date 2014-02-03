# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Account, Building, Defense, Planet, Research, Ship

def item_update(req):
    """
    """
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
        account = obj.planet.account
    elif 'defense' == item_type:
        obj = Defense.objects.select_related('planet__account').get(pk=item_id)
        account = obj.planet.account
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

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


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

    return HttpResponseRedirect(req.META['HTTP_REFERER'])


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

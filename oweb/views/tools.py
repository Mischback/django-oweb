"""Provides some general, account-related tools"""
# Python imports
from math import ceil
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
# app imports
from oweb.models.building import Planet, Supply12
from oweb.models.research import Research113

def tools_energy(req, account_id):
    """Shows some energy related information"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # fetch the account and the current planet
    try:
        planets = Planet.objects.select_related('account').filter(account_id=account_id)
        account = planets.first().account
    except Planet.DoesNotExist:
        raise Http404

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise Http404

    planet_ids = planets.values_list('id', flat=True)
    fusion_list = get_list_or_404(Supply12, planet_id__in=planet_ids)
    energy = get_object_or_404(Research113, account_id=account_id)

    # determine the average fusion reactor and maximum fusion reactor
    max_fusion = 0
    average_fusion = 0
    for f in fusion_list:
        average_fusion += f.level
        if f.level > max_fusion:
            max_fusion = f.level
    average_fusion = ceil(average_fusion / len(planet_ids))

    return render(req, 'oweb/tools_energy.html',
        {
            'account': account,
            'planets': planets
        }
    )

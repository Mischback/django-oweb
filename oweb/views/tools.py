"""Provides some general, account-related tools"""
# Python imports
from math import ceil
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect, render
# app imports
from oweb.exceptions import OWebDoesNotExist, OWebAccountAccessViolation
from oweb.models.planet import Planet
from oweb.models.building import Supply12
from oweb.models.research import Research113
from oweb.libs.production import get_fusion_production
from oweb.libs.costs import costs_onepointeight_total, costs_two_total
from oweb.libs.queue import get_mse
from oweb.libs.shortcuts import get_list_or_404, get_object_or_404

def tools_energy(req, account_id, energy_level=None, fusion_level=None):
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
        raise OWebDoesNotExist
    except AttributeError:
        raise OWebDoesNotExist

    # checks, if this account belongs to the authenticated user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    planet_ids = planets.values_list('id', flat=True)

    if not fusion_level:
        fusion_list = get_list_or_404(Supply12, astro_object_id__in=planet_ids)
        # determine the average fusion reactor and maximum fusion reactor
        max_fusion = 0
        average_fusion = 0
        for f in fusion_list:
            average_fusion += f.level
            if f.level > max_fusion:
                max_fusion = f.level
        fusion_level = ceil(average_fusion / len(planet_ids))
        fusion_base_cost = f.base_cost
    else:
        fusion_base_cost = Supply12.base_cost
    fusion_level = int(fusion_level)

    if not energy_level:
        energy = get_object_or_404(Research113, account_id=account_id)
        energy_level = energy.level
        energy_base_cost = energy.base_cost
    else:
        energy_level = int(energy_level)
        energy_base_cost = Research113.base_cost

    # calculate the costs of the current fusion plant
    current_fusion_cost = costs_onepointeight_total(fusion_base_cost, fusion_level)
    current_fusion_cost = get_mse(current_fusion_cost, (account.trade_metal, account.trade_crystal, account.trade_deut))

    # calculate the costs of the current energy technology
    current_energy_cost = costs_two_total(energy_base_cost, energy_level)
    current_energy_cost = get_mse(current_energy_cost, (account.trade_metal, account.trade_crystal, account.trade_deut))

    # calculate the production of the fusion plant
    this_prod = int(get_fusion_production(fusion_level, energy=energy_level)[3])

    fusion_matrix = []
    for i in range(0, 5):
        f = fusion_level + i

        # calculate the costs of this fusion plant
        f_cost = costs_onepointeight_total(fusion_base_cost, f)
        f_cost = get_mse(f_cost, (account.trade_metal, account.trade_crystal, account.trade_deut)) - current_fusion_cost

        et_range = []
        for j in range(0, 5):
            et = energy_level + j

            # calculate the costs of this energy tech
            et_cost = costs_two_total(energy_base_cost, et)
            et_cost = (get_mse(et_cost, (account.trade_metal, account.trade_crystal, account.trade_deut)) - current_energy_cost) / len(planet_ids)

            # total costs of this combination
            next_cost = f_cost + et_cost

            # calculate the production of this combination
            next_prod = int(get_fusion_production(f, energy=et)[3])
            next_prod_gain = int(next_prod - this_prod)

            # calculate the "score" of this combination
            # COSTS / PRODUCTION_GAIN
            if next_prod_gain != 0:
                next_ratio = next_cost / next_prod_gain
            else:
                next_ratio = 0

            et_range.append((
                et,
                next_prod,
                next_prod_gain,
                next_cost,
                next_ratio
            ))

        fusion_matrix.append((int(f), et_range))

    return render(req, 'oweb/tools_energy.html',
        {
            'account': account,
            'planets': planets,
            'fusion_matrix': fusion_matrix,
            'energy_level': energy_level,
            'fusion_level': fusion_level,
        }
    )

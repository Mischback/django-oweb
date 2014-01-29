# Django imports
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Supply1, Supply2, Supply3, Supply4, Supply12, Civil212, Research113, Research122
from oweb.libs.production import get_metal_production, get_crystal_production, get_deuterium_production
from oweb.libs.costs import costs_onepointfive, costs_onepointsix, costs_onepointeight


def get_metal_equivalent(ressources, trade):
    """
    @brief  Returns the equivalent of a given ressource tupel
    @param  ressources TUPEL
    """
    mse = ressources[0]
    mse = mse + (trade[0] / trade[1] * ressources[1])
    mse = mse + (trade[0] / trade[2] * ressources[2])

    return int(mse)


def get_planet_queue(planet, speed, 
    supply1=None,
    supply2=None,
    supply3=None,
    supply4=None,
    supply12=None,
    civil212=None,
    research113=None,
    research122=None):
    """
    """
    # Metal
    if not supply1:
        supply1 = get_object_or_404(Supply1, planet=planet.id)
    # Crystal
    if not supply2:
        supply2 = get_object_or_404(Supply2, planet=planet.id)
    # Deut
    if not supply3:
        supply3 = get_object_or_404(Supply3, planet=planet.id)
    # get energy production
    if not supply4:
        supply4 = get_object_or_404(Supply4, planet=planet.id)
    if not supply12:
        supply12 = get_object_or_404(Supply12, planet=planet.id)
    if not civil212:
        civil212 = get_object_or_404(Civil212, planet=planet.id)
    if not research113:
        research113 = get_object_or_404(Research113, account=planet.account.id)
    # plasma bonus
    if not research122:
        research122 = get_object_or_404(Research122, account=planet.account.id)

    trade = (planet.account.trade_metal, planet.account.trade_crystal, planet.account.trade_deut)

    this_metal_prod = get_metal_production(supply1.level, speed=speed)
    this_metal_prod_mse = get_metal_equivalent(this_metal_prod, trade)
    this_crystal_prod = get_crystal_production(supply2.level, speed=speed)
    this_crystal_prod_mse = get_metal_equivalent(this_crystal_prod, trade)
    this_deut_prod = get_deuterium_production(supply3.level, speed=speed)
    this_deut_prod_mse = get_metal_equivalent(this_deut_prod, trade)

    queue = []
    for i in range(1, 6):
        next_cost = costs_onepointfive(supply1.base_cost, supply1.level, offset=i)
        next_cost_mse = get_metal_equivalent(next_cost, trade)
        next_metal_prod = get_metal_production(supply1.level + i, speed=speed)
        next_metal_prod_mse = get_metal_equivalent(next_metal_prod, trade)

        try:
            next_score = int(next_cost_mse / (next_metal_prod_mse - this_metal_prod_mse))
        except ZeroDivisionError:
            next_score = 1000000000000

        queue.append((next_score, supply1.name, supply1.level + i))

        this_metal_prod_mse = next_metal_prod_mse

        next_crystal_cost = costs_onepointsix(supply2.base_cost, supply2.level, offset=i)
        next_crystal_cost_mse = get_metal_equivalent(next_crystal_cost, trade)
        next_crystal_prod = get_crystal_production(supply2.level + i, speed=speed)
        next_crystal_prod_mse = get_metal_equivalent(next_crystal_prod, trade)

        try:
            next_score = int(next_cost_mse / (next_crystal_prod_mse - this_crystal_prod_mse))
        except ZeroDivisionError:
            next_score = 1000000000000

        queue.append((next_score, supply2.name, supply2.level + i))

        this_crystal_prod_mse = next_crystal_prod_mse

        next_deut_cost = costs_onepointeight(supply3.base_cost, supply3.level, offset=i)
        next_deut_cost_mse = get_metal_equivalent(next_deut_cost, trade)
        next_deut_prod = get_deuterium_production(supply3.level + i, temp=planet.min_temp + 40, speed=speed)
        next_deut_prod_mse = get_metal_equivalent(next_deut_prod, trade)

        try:
            next_score = int(next_cost_mse / (next_deut_prod_mse - this_deut_prod_mse))
        except ZeroDivisionError:
            next_score = 1000000000000

        queue.append((next_score, supply3.name, supply3.level + i))

        this_deut_prod_mse = next_deut_prod_mse

    queue.sort()

    return queue

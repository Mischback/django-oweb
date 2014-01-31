# Django imports
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Supply1, Supply2, Supply3, Supply4, Supply12, Civil212, Research113, Research122
from oweb.libs.production import get_metal_production, get_crystal_production, get_deuterium_production, get_plasma_bonus
from oweb.libs.costs import costs_onepointfive, costs_onepointsix, costs_onepointeight, costs_two


def get_mse(ressources, trade):
    """
    @brief  Returns the equivalent of a given ressource tupel
    @param  ressources TUPEL
    """
    mse = ressources[0]
    mse = mse + (trade[0] / float(trade[1]) * ressources[1])
    mse = mse + (trade[0] / float(trade[2]) * ressources[2])

    return int(mse)


def queue_item(name, level,                 # which item?
    next_cost, next_prod, this_prod, trade, # used for calculation
    planet
    ):
    """
    """
    # calculate MSE
    next_cost_mse = get_mse(next_cost, trade)
    # determine score
    try:
        score = int(next_cost_mse / (next_prod - this_prod))
    except ZeroDivisionError:
        score = 1000000000000

    return (score,
        {
            'name': name, 
            'level': level,
            'planet': planet,
        })


def get_planet_queue(planet, speed, 
    supply1=None,
    supply2=None,
    supply3=None,
    supply4=None,
    supply12=None,
    civil212=None,
    research113=None):
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

    trade = (planet.account.trade_metal, planet.account.trade_crystal, planet.account.trade_deut)

    this_metal_prod = get_mse(
        get_metal_production(supply1.level, speed=speed),
        trade
    )
    this_crystal_prod = get_mse(
        get_crystal_production(supply2.level, speed=speed),
        trade
    )
    this_deut_prod = get_mse(
        get_deuterium_production(supply3.level, temp=planet.min_temp + 40, speed=speed),
        trade
    )

    queue = []
    for i in range(1, 6):
        next_cost = costs_onepointfive(supply1.base_cost, supply1.level, offset=i)
        next_metal_prod = get_mse(
            get_metal_production(supply1.level + i, speed=speed),
            trade
        )

        queue.append(queue_item(
            supply1.name,
            supply1.level + i,
            next_cost,
            next_metal_prod,
            this_metal_prod,
            trade,
            planet))

        this_metal_prod = next_metal_prod

        next_cost = costs_onepointsix(supply2.base_cost, supply2.level, offset=i)
        next_crystal_prod = get_mse(
            get_crystal_production(supply2.level + i, speed=speed),
            trade
        )

        queue.append(queue_item(
            supply2.name,
            supply2.level + i,
            next_cost,
            next_crystal_prod,
            this_crystal_prod,
            trade,
            planet))

        this_crystal_prod = next_crystal_prod

        next_cost = costs_onepointfive(supply3.base_cost, supply3.level, offset=i)
        next_deut_prod = get_mse(
            get_deuterium_production(supply3.level + i, temp=planet.min_temp + 40, speed=speed),
            trade
        )

        queue.append(queue_item(
            supply3.name,
            supply3.level + i,
            next_cost,
            next_deut_prod,
            this_deut_prod,
            trade,
            planet))

        this_deut_prod = next_deut_prod

    queue.sort()

    return queue


def get_plasma_queue(account, research122=None, production=(0, 0, 0, 0)):
    """
    """
    if not research122:
        research122 = get_object_or_404(Research122, account=account.id)

    trade = (account.trade_metal, account.trade_crystal, account.trade_deut)

    this_prod = get_mse(
        get_plasma_bonus(research122.level, production[0], production[1]),
        trade
    )

    queue = []

    for i in range(1, 6):
        next_cost = costs_two(research122.base_cost, research122.level, offset=i)
        next_prod = get_mse(
            get_plasma_bonus(research122.level + i, production[0], production[1]),
            trade
        )

        queue.append(queue_item(
            research122.name,
            research122.level + i,
            next_cost,
            next_prod,
            this_prod,
            trade,
            account))

        this_prod = next_prod

    return queue

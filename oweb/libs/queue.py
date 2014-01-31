# Django imports
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Supply1, Supply2, Supply3, Supply4, Supply12, Station14, Station15, Civil212, Research113, Research122
from oweb.libs.production import get_metal_production, get_crystal_production, get_deuterium_production, get_plasma_bonus, get_capacity, get_sat_production, get_energy_production
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


def queue_item(id, name, level,
    next_cost, next_prod, this_prod, trade,
    this_capacity, next_capacity, next_cap_cost, next_cap_time,
    required_sats,
    planet
    ):
    """
    """
    # init some vars... 
    # This catches some issues with Plasma research
    need_capacity = 0
    this_build_time = 0

    # calculate MSE
    next_cost_mse = get_mse(next_cost, trade)

    # calc production gain
    gain = next_prod - this_prod

    # calc amortisation time
    amortisation = next_cost_mse / float(gain)

    # calculate building time
    if this_capacity and next_capacity:
        ress = next_cost[0] + next_cost[1] + next_cost[2]
        this_build_time = ress / float(this_capacity)
        next_build_time = ress / float(next_capacity)
        cap_bonus = (this_build_time - (next_cap_time + next_build_time)) * gain
        if cap_bonus < next_cap_cost:
            need_capacity = 0
        else:
            need_capacity = 1

    # determine score
    try:
        score = int(next_cost_mse / gain)
    except ZeroDivisionError:
        score = 1000000000000

    # normalize required sats
    if required_sats < 0:
        required_sats = 0

    return (score,
        required_sats,
        this_build_time,
        need_capacity,
        {
            'id': id,
            'name': name, 
            'level': level,
            'gain': gain,
            'planet': planet,
        })


def get_planet_queue(planet,
    speed=None, 
    trade=None,
    supply1=None,
    supply2=None,
    supply3=None,
    supply4=None,
    supply12=None,
    station14=None,
    station15=None,
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
    # Solar
    if not supply4:
        supply4 = get_object_or_404(Supply4, planet=planet.id)
    # Fusion
    if not supply12:
        supply12 = get_object_or_404(Supply12, planet=planet.id)
    # Robo
    if not station14:
        station14 = get_object_or_404(Station14, planet=planet.id)
    # Nani
    if not station15:
        station15 = get_object_or_404(Station15, planet=planet.id)
    # Sat
    if not civil212:
        civil212 = get_object_or_404(Civil212, planet=planet.id)
    # Energy
    if not research113:
        research113 = get_object_or_404(Research113, account=planet.account.id)
    # account speed
    if not speed:
        speed = planet.account.speed
    # trade rates
    if not trade:
        trade = (planet.account.trade_metal, planet.account.trade_crystal, planet.account.trade_deut)

    # calculate current metal production
    this_metal_prod = get_metal_production(supply1.level, speed=speed)
    this_metal_prod_mse = get_mse(
        this_metal_prod,
        trade
    )
    # calculate current crystal production
    this_crystal_prod = get_crystal_production(supply2.level, speed=speed)
    this_crystal_prod_mse = get_mse(
        this_crystal_prod,
        trade
    )
    # calculate current deuterium production
    this_deut_prod = get_deuterium_production(supply3.level, temp=planet.min_temp + 40, speed=speed)
    this_deut_prod_mse = get_mse(
        this_deut_prod,
        trade
    )

    # calculate planet's energy
    sol, fus, sat = get_energy_production(
        supply4.level,
        supply12.level,
        civil212.count,
        temp=planet.min_temp + 40,
        energy=research113.level,
        max_performance=True)
    planet_energy = tuple(sum(x) for x in zip(sol, fus, sat))[3]
    planet_energy += this_metal_prod[3]
    planet_energy += this_crystal_prod[3]
    planet_energy += this_deut_prod[3]

    # how much can one sat produce?
    sat_prod = get_sat_production(1, temp=planet.min_temp + 40)[3]

    # calculate current capacity (ress per hour)
    this_capacity = get_capacity(station14.level, station15.level, speed)
    if station14.level > 9:
        next_capacity = get_capacity(station14.level, station15.level + 1, speed)
        next_cap_cost = costs_two(station15.base_cost, station15.level, offset=1)
    else:
        next_capacity = get_capacity(station14.level + 1, station15.level, speed)
        next_cap_cost = costs_two(station14.base_cost, station14.level, offset=1)
    next_cap_cost_mse = get_mse(next_cap_cost, trade)
    next_cap_time = (next_cap_cost[0] + next_cap_cost[1] + next_cap_cost[2]) / float(this_capacity)

    queue = []
    for i in range(1, 6):
        # *** Metal Mine
        # cost of this level
        next_cost = costs_onepointfive(supply1.base_cost, supply1.level, offset=i)
        # production of this level
        next_metal_prod = get_metal_production(supply1.level + i, speed=speed)
        next_metal_prod_mse = get_mse(
            next_metal_prod,
            trade
        )
        # energy (number of sats to determine the energy consumption)
        this_energy = -1 * (planet_energy + next_metal_prod[3] - this_metal_prod[3])
        required_sats = this_energy / sat_prod

        queue.append(queue_item(
            supply1.id,
            supply1.name,
            supply1.level + i,
            next_cost,
            next_metal_prod_mse,
            this_metal_prod_mse,
            trade,
            this_capacity,
            next_capacity,
            next_cap_cost_mse,
            next_cap_time,
            required_sats,
            planet))

        this_metal_prod_mse = next_metal_prod_mse

        # *** Crystal Mine
        # cost of this level
        next_cost = costs_onepointsix(supply2.base_cost, supply2.level, offset=i)
        # production of this level
        next_crystal_prod = get_crystal_production(supply2.level + i, speed=speed)
        next_crystal_prod_mse = get_mse(
            next_crystal_prod,
            trade
        )
        # energy (number of sats to determine the energy consumption)
        this_energy = -1 * (planet_energy + next_crystal_prod[3] - this_crystal_prod[3])
        required_sats = this_energy / sat_prod

        queue.append(queue_item(
            supply2.id,
            supply2.name,
            supply2.level + i,
            next_cost,
            next_crystal_prod_mse,
            this_crystal_prod_mse,
            trade,
            this_capacity,
            next_capacity,
            next_cap_cost_mse,
            next_cap_time,
            required_sats,
            planet))

        this_crystal_prod_mse = next_crystal_prod_mse

        # *** Deuterium Synthesizer
        # cost of this level
        next_cost = costs_onepointfive(supply3.base_cost, supply3.level, offset=i)
        # production of this level
        next_deut_prod = get_deuterium_production(supply3.level + i, temp=planet.min_temp + 40, speed=speed)
        next_deut_prod_mse = get_mse(
            next_deut_prod,
            trade
        )
        # energy (number of sats to determine the energy consumption)
        this_energy = -1 * (planet_energy + next_deut_prod[3] - this_deut_prod[3])
        required_sats = this_energy / sat_prod

        queue.append(queue_item(
            supply3.id,
            supply3.name,
            supply3.level + i,
            next_cost,
            next_deut_prod_mse,
            this_deut_prod_mse,
            trade,
            this_capacity,
            next_capacity,
            next_cap_cost_mse,
            next_cap_time,
            required_sats,
            planet))

        this_deut_prod_mse = next_deut_prod_mse

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
            research122.id,
            research122.name,
            research122.level + i,
            next_cost,
            next_prod,
            this_prod,
            trade,
            None,
            None,
            None,
            None,
            0,
            account))

        this_prod = next_prod

    return queue

# Python imports
from math import floor, ceil
# Django imports
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Supply1, Supply2, Supply3, Supply4, Supply12, Civil212, Research113, Research122

def get_metal_production(level, performance=1.0, speed=1):
    """
    @brief  Returns the production of a metalmine with a given level
    @param  level INTEGER The level of the building
    @param  performance FLOAT The performance of the mine
    @param  speed INTEGER The universe's speed modifier (default: 1)
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = floor(30 * level * 1.1 ** level * performance * speed)
    energy = ceil(10 * level * 1.1 ** level * performance)

    return (production, 0, 0, -energy)


def get_crystal_production(level, performance=1.0, speed=1):
    """
    @brief  Returns the production of a crystalmine with a given level
    @param  level INTEGER The level of the building
    @param  performance FLOAT The performance of the mine
    @param  speed INTEGER The universe's speed modifier (default: 1)
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = floor(20 * level * 1.1 ** level * performance * speed)
    energy = ceil(10 * level * 1.1 ** level * performance)

    return (0, production, 0, -energy)


def get_deuterium_production(level, temp=0, performance=1.0, speed=1):
    """
    @brief  Returns the production of a crystalmine with a given level
    @param  level INTEGER The level of the building
    @param  performance FLOAT The performance of the mine
    @param  speed INTEGER The universe's speed modifier (default: 1)
    @param  temp INTEGER Maximum temperature of the planet
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = floor(10 * level * 1.1 ** level * (1.44 - 0.004 * temp) * performance * speed)
    energy = ceil(20 * level * 1.1 ** level * performance)

    return (0, 0, production, -energy)


def get_solar_production(level, performance=1.0):
    """
    @brief  Returns the energy production of the solar plant
    @param  level INTEGER The level of the building
    @param  performance FLOAT The performance of the mine
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = round(floor(20 * level * 1.1 ** level) * performance)

    return (0, 0, 0, production)


def get_fusion_production(level, performance=1.0, speed=1, energy=3):
    """
    @brief  Returns the energy production of the fusion plant
    @param  level INTEGER The level of the building
    @param  performance FLOAT The performance of the mine
    @param  speed INTEGER The universe's speed modifier (default: 1)
    @param  energy INTEGER The level of energy research
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = round(floor(30 * level * (1.05 + energy * 0.01) ** level) * performance)
    consumption = ceil(10 * level * 1.1 ** level * performance) * speed

    return (0, 0, -consumption, production)


def get_sat_production(count, temp=0):
    """
    @brief  Returns the energy production of Solar Satellites
    @param  count INTEGER The number of satellites
    @param  temp INTEGER Maximum temperature of the planet
    @retval TUPEL A tupel with metal, crystal, deuterium and energy values
    """
    production = round(floor((temp + 140) / 6) * count)

    return (0, 0, 0, production)


def get_energy_production(solar_level, fusion_level, sat_count,
    solar_perf=1.0, fusion_perf=1.0,
    temp=0,
    speed=1,
    energy=3,
    max_performance=False):
    """
    """
    if max_performance:
        solar_prod = get_solar_production(solar_level)
        fusion_prod = get_fusion_production(fusion_level, speed=speed, energy=energy)
    else:
        solar_prod = get_solar_production(solar_level, performance=solar_perf)
        fusion_prod = get_fusion_production(fusion_level, performance=fusion_perf, speed=speed, energy=energy)

    sat_prod = get_sat_production(sat_count, temp=temp)

    return solar_prod, fusion_prod, sat_prod


def get_plasma_bonus(plasma_level, metal, crystal):
    metalbonus = floor(metal * 0.01 * plasma_level)
    crystalbonus = floor(crystal * 0.0066 * plasma_level)

    return (metalbonus, crystalbonus, 0, 0)


def get_planet_production(planet, speed,
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
    prod = []

    # get production of the mines
    # Metal
    if not supply1:
        supply1 = get_object_or_404(Supply1, planet=planet.id)
    metal_prod = get_metal_production(supply1.level,
        performance=supply1.performance,
        speed=speed)

    # Crystal
    if not supply2:
        supply2 = get_object_or_404(Supply2, planet=planet.id)
    crystal_prod = get_crystal_production(supply2.level,
        performance=supply2.performance,
        speed=speed)

    # Deut
    if not supply3:
        supply3 = get_object_or_404(Supply3, planet=planet.id)
    deut_prod = get_deuterium_production(supply3.level,
        temp=planet.min_temp + 40,
        performance=supply3.performance,
        speed=speed)

    # get energy production
    if not supply4:
        supply4 = get_object_or_404(Supply4, planet=planet.id)
    if not supply12:
        supply12 = get_object_or_404(Supply12, planet=planet.id)
    if not civil212:
        civil212 = get_object_or_404(Civil212, planet=planet.id)
    if not research113:
        research113 = get_object_or_404(Research113, account=planet.account.id)
    solar_prod, fusion_prod, sat_prod = get_energy_production(
        supply4.level, supply12.level, civil212.count,
        solar_perf=supply4.performance,
        fusion_perf=supply12.performance,
        temp=planet.min_temp + 40,
        speed=speed,
        energy=research113.level)

    # plasma bonus
    if not research122:
        research122 = get_object_or_404(Research122, account=planet.account.id)
    plasma_bonus = get_plasma_bonus(research122.level, metal_prod[0], crystal_prod[1])

    # add base income
    base_income = (30 * speed, 15 * speed, 0, 0)

    # sum it up
    prod = tuple(sum(x) for x in zip(
        metal_prod, crystal_prod, deut_prod,
        solar_prod, fusion_prod, sat_prod,
        plasma_bonus, base_income
    ))

    return prod


def get_planet_capacity(planet, speed=None):
    """
    """
    if not speed:
        speed = planet.account.speed

    robo = get_object_or_404(Station14, planet=planet.id)
    nani = get_object_or_404(Station15, planet=planet.id)

    return get_capacity(robo.level, nani.level, speed)


def get_capacity(robo, nani, speed):
    """
    """
    return (2500 * speed * (1 + robo) * 2 ** nani)

"""
Contains the functions to calculate the production of mines.

The functions in this file are used to calculate the production related stuff.

Please note, that most of the functions return a tuple with four values:
``(metal, crystal, deuterium, energy)``

For every function, these four values are populated, i.e. if you calculate the
production of a metal mine, you will get a tuple with a positive ``metal`` value,
a negative ``energy`` value and ``crystal`` and ``deut`` will be zero.
"""
# Python imports
from math import floor, ceil
# Django imports
from django.shortcuts import get_object_or_404
# app imports
from oweb.models import Supply1, Supply2, Supply3, Supply4, Supply12, Civil212, Research113, Research122

def get_metal_production(level, performance=1.0, speed=1):
    """Returns the production of a metalmine with a given level

    :param level: The level of the building
    :type level: int
    :param performance: The performance of the mine
    :type performance: float
    :param speed: The universe's speed modifier (default: 1)
    :type speed: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = floor(30 * level * 1.1 ** level * performance * speed)
    energy = ceil(10 * level * 1.1 ** level * performance)

    return (production, 0, 0, -energy)


def get_crystal_production(level, performance=1.0, speed=1):
    """Returns the production of a crystalmine with a given level

    :param level: The level of the building
    :type level: int
    :param performance: The performance of the mine
    :type performance: float
    :param speed: The universe's speed modifier (default: 1)
    :type speed: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = floor(20 * level * 1.1 ** level * performance * speed)
    energy = ceil(10 * level * 1.1 ** level * performance)

    return (0, production, 0, -energy)


def get_deuterium_production(level, temp=0, performance=1.0, speed=1):
    """Returns the production of a crystalmine with a given level

    :param level: The level of the building
    :type level: int
    :param temp: The planet's maximum temperature
    :type temp: int
    :param performance: The performance of the mine
    :type performance: float
    :param speed: The universe's speed modifier (default: 1)
    :type speed: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = floor(10 * level * 1.1 ** level * (1.44 - 0.004 * temp) * performance * speed)
    energy = ceil(20 * level * 1.1 ** level * performance)

    return (0, 0, production, -energy)


def get_solar_production(level, performance=1.0):
    """Returns the energy production of the solar plant

    :param level: The level of the building
    :type level: int
    :param performance: The performance of the mine
    :type performance: float
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = round(floor(20 * level * 1.1 ** level) * performance)

    return (0, 0, 0, production)


def get_fusion_production(level, performance=1.0, speed=1, energy=3):
    """Returns the energy production of the fusion plant

    :param level: The level of the building
    :type level: int
    :param performance: The performance of the mine
    :type performance: float
    :param speed: The universe's speed modifier (default: 1)
    :type speed: int
    :param energy: The level of energy research
    :type energy: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = round(floor(30 * level * (1.05 + energy * 0.01) ** level) * performance)
    consumption = ceil(10 * level * 1.1 ** level * performance) * speed

    return (0, 0, -consumption, production)


def get_sat_production(count, temp=0):
    """Returns the energy production of Solar Satellites

    :param count: The number of satellites
    :type count: int
    :param temp: Maximum temperature of the planet
    :type temp: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values
    """
    production = round(floor((temp + 140) / 6) * count)

    return (0, 0, 0, production)


def get_energy_production(solar_level, fusion_level, sat_count,
    solar_perf=1.0, fusion_perf=1.0,
    temp=0,
    speed=1,
    energy=3,
    max_performance=False):
    """Returns the energy productions of a given set of buildings and sats

    :param solar_level: The level of the solar plant
    :type solar_level: int
    :param fusion_level: The level of the fusion plant
    :type fusion_level: int
    :param sat_count: The number of SolarSatellites
    :type sat_count: int
    :param solar_perf: The performance of the solar plant (default: 1.0)
    :type solar_perf: float
    :param fusion_perf: The performance of the fusion plant (default: 1.0)
    :type fusion_perf: float
    :param temp: The maximum temperature of the planet
    :type temp: int
    :param speed: The universe speed (default: 1)
    :type speed: int
    :param energy: The level of energy technology (default: 3)
    :type energy: int
    :param max_performance: Calculate the actual production or the maximum production
    :type max_performance: bool
    :returns: tuple -- solar_prod, tuple -- fusion_prod, tuple -- sat_prod

    **Please note, that this function returns three values!**
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
    """Returns the bonus production from Plasma technology

    :param plasma_level: Level of Plasma Technology
    :type plasma_level: int
    :param metal: Current metal production (from mines)
    :type metal: int
    :param crystal: Current crystal production (from mines)
    :type crystal: int
    :returns: tuple -- A tuple with metal, crystal, deuterium and energy values

    The OGame method to calculate this value: Take the production of metal mines
    and crystal mines (without base income) and apply the plasma bonus.
    """
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
    """Returns the total production of a Planet

    :param planet: The planet in question
    :type planet: Planet object
    :param speed: This universe's speed
    :type speed: int
    :param supply1: This planet's metal mine (default: None)
    :type supply1: Supply1 object
    :param supply2: This planet's crystal mine (default: None)
    :type supply2: Supply2 object
    :param supply3: This planet's deuterium synthesizer (default: None)
    :type supply3: Supply3 object
    :param supply4: This planet's solar plant (default: None)
    :type supply4: Supply4 object
    :param supply12: This planet's fusion plant (default: None)
    :type supply12: Supply12 object
    :param civil212: This planet's solar satellites (default: None)
    :type civil212: Civil212 object
    :param research113: This account's energy technology (default: None)
    :type research113: Research113 object
    :param research122: This account's plasma technology (default: None)
    :type research122: Research122 object

    Most of the parameters of this function are optional, but necessary. If
    they are not specified while calling this function, they will be fetched.

    Performancewise it is useful to provide these values, because it will save
    database queries. The queries made within this function are in no way
    efficient. Every item is fetched on its own.
    """
    prod = []

    # get production of the mines
    # Metal
    if not supply1:
        supply1 = get_object_or_404(Supply1, astro_object=planet.id)
    metal_prod = get_metal_production(supply1.level,
        performance=supply1.performance,
        speed=speed)

    # Crystal
    if not supply2:
        supply2 = get_object_or_404(Supply2, astro_object=planet.id)
    crystal_prod = get_crystal_production(supply2.level,
        performance=supply2.performance,
        speed=speed)

    # Deut
    if not supply3:
        supply3 = get_object_or_404(Supply3, astro_object=planet.id)
    deut_prod = get_deuterium_production(supply3.level,
        temp=planet.max_temp,
        performance=supply3.performance,
        speed=speed)

    # get energy production
    if not supply4:
        supply4 = get_object_or_404(Supply4, astro_object=planet.id)
    if not supply12:
        supply12 = get_object_or_404(Supply12, astro_object=planet.id)
    if not civil212:
        civil212 = get_object_or_404(Civil212, astro_object=planet.id)
    if not research113:
        research113 = get_object_or_404(Research113, account=planet.account.id)
    solar_prod, fusion_prod, sat_prod = get_energy_production(
        supply4.level, supply12.level, civil212.count,
        solar_perf=supply4.performance,
        fusion_perf=supply12.performance,
        temp=planet.max_temp,
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
    """Returns the planet's capacity, which means: How many ressources can be used in one hour

    :param planet: The planet in question
    :type planet: Planet object
    :param speed: The account's speed (default: None)
    :type speed: int
    :returns: int -- The current capacity of this planet

    This function will fetch the relevant objects (Nani and Robo) on its own.

    Please note that the capacity is returned in total ressources, not MSE.
    """
    if not speed:
        speed = planet.account.speed

    robo = get_object_or_404(Station14, astro_object=planet.id)
    nani = get_object_or_404(Station15, astro_object=planet.id)

    return get_capacity(robo.level, nani.level, speed)


def get_capacity(robo, nani, speed):
    """Returns the capacity for a given combination of Nanite and Robotics Factory

    :param robo: Level of the Robotics Factory
    :type robo: int
    :param nani: Level of the Nanite Factory
    :type nani: int
    :param speed: The account's speed
    :type speed: int
    :returns: int -- The capacity of this combination
    """
    return (2500 * speed * (1 + robo) * 2 ** nani)

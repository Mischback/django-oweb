"""
@file   costs.py
@brief  Contains functions to calculate costs

The functions in this file are used to calculate the costs of buildings and
researches. There are certain categories of these items; the only difference
is the base factor.

Note: Costs in OGame are growing exponentially.

This library contains functions to calculate the costs of a given level of a
building/research and functions to calculate the total costs of building/
research with a given level (the sum of all seperate levels). Functions of the
latter group are suffixed with "_total".

The formulas (and where to use them) were taken from http://owiki.de. Additional
mathematic formulas were taken from Wikipedia.
"""

def costs(base_cost, modifier, level):
    """
    @brief  Generic functiont to calculate the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  modifier FLOAT The base factor to be used
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium
    """
    metal = (base_cost[0] / modifier) * modifier ** level
    crystal = (base_cost[1] / modifier) * modifier ** level
    deut = (base_cost[2] / modifier) * modifier ** level

    return (int(metal), int(crystal), int(deut))


def costs_total(base_cost, modifier, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  modifier FLOAT The base factor to be used
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium
    """
    geo = float(1 - modifier ** (level + 1)) / float(1 - modifier)
    metal = (base_cost[0] / modifier) * geo - (base_cost[0] / modifier)
    crystal = (base_cost[1] / modifier) * geo - (base_cost[1] / modifier)
    deut = (base_cost[2] / modifier) * geo - (base_cost[2] / modifier)
    return (int(metal), int(crystal), int(deut))


def costs_onepointfive(base_cost, current_level, offset=1):
    """
    @brief  Returns a tupel with the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  current_level INTEGER The current level of the item
    @param  offset INTEGER The offset from the current level
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.5
    """
    return costs(base_cost, 1.5, current_level + offset)


def costs_onepointfive_total(base_cost, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.5
    """
    return costs_total(base_cost, 1.5, level)


def costs_onepointsix(base_cost, current_level, offset=1):
    """
    @brief  Returns a tupel with the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  current_level INTEGER The current level of the item
    @param  offset INTEGER The offset from the current level
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.6
    """
    return costs(base_cost, 1.6, current_level + offset)


def costs_onepointsix_total(base_cost, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.6
    """
    return costs_total(base_cost, 1.6, level)


def costs_onepointeight(base_cost, current_level, offset=1):
    """
    @brief  Returns a tupel with the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  current_level INTEGER The current level of the item
    @param  offset INTEGER The offset from the current level
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.8
    """
    return costs(base_cost, 1.8, current_level + offset)


def costs_onepointeight_total(base_cost, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 1.8
    """
    return costs_total(base_cost, 1.8, level)


def costs_two(base_cost, current_level, offset=1):
    """
    @brief  Returns a tupel with the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  current_level INTEGER The current level of the item
    @param  offset INTEGER The offset from the current level
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 2.0
    """
    return costs(base_cost, 2.0, current_level + offset)


def costs_two_total(base_cost, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 2.0
    """
    return costs_total(base_cost, 2.0, level)


def costs_twopointthree(base_cost, current_level, offset=1):
    """
    @brief  Returns a tupel with the costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  current_level INTEGER The current level of the item
    @param  offset INTEGER The offset from the current level
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 2.3
    """
    return costs(base_cost, 2.3, current_level + offset)


def costs_twopointthree_total(base_cost, level):
    """
    @brief  Generic functiont to calculate the total costs of a given level
    @param  base_cost TUPEL The base costs of the item
    @param  level INTEGER The level to be calculated
    @retval TUPEL The costs in metal, crystal and deuterium

    This function is used for buildings/researches with a base factor of 2.3
    """
    return costs_total(base_cost, 2.3, level)

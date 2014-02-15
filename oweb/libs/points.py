# Django imports
from django.shortcuts import get_list_or_404
# app imports
from oweb.models.planet import Moon
from oweb.models.building import Building, Supply1, Supply2, Supply3, Supply4, Supply12
from oweb.models.defense import Defense
from oweb.models.ship import Ship, Civil202, Civil203, Civil208, Civil210, Civil212
from oweb.models.research import Research

def get_planet_points(planet):
    buildings = get_list_or_404(Building, astro_object=planet)
    defense = get_list_or_404(Defense, astro_object=planet)

    other_points = 0
    production_points = 0
    defense_points = 0

    for b in buildings:
        this_building_cost = b.get_total_cost()
        this_building_points = this_building_cost[0] + this_building_cost[1] + this_building_cost[2]

        if b.content_type.model_class() in [Supply1, Supply2, Supply3, Supply4, Supply12]:
            production_points += this_building_points
        else:
            other_points += this_building_points

    for d in defense:
        this_defense = d.as_real_class()
        this_defense_points = this_defense.count * (this_defense.cost[0] + this_defense.cost[1] + this_defense.cost[2])

        defense_points += this_defense_points

    planet_points = production_points + other_points + defense_points

    try:
        moon = Moon.objects.get(planet=planet)
        moon_points, moon_buildings, moon_defense = get_moon_points(moon)
    except Moon.DoesNotExist:
        moon_points = 0
        moon_buildings = 0
        moon_defense = 0

    return planet_points, production_points, other_points, defense_points, moon_points, moon_buildings, moon_defense


def get_moon_points(moon):
    buildings = get_list_or_404(Building, astro_object=moon)
    defense = get_list_or_404(Defense, astro_object=moon)

    other_points = 0
    defense_points = 0

    for b in buildings:
        this_building_cost = b.get_total_cost()
        this_building_points = this_building_cost[0] + this_building_cost[1] + this_building_cost[2]

        other_points += this_building_points

    for d in defense:
        this_defense = d.as_real_class()
        this_defense_points = this_defense.count * (this_defense.cost[0] + this_defense.cost[1] + this_defense.cost[2])

        defense_points += this_defense_points

    return other_points + defense_points, other_points, defense_points


def get_ship_points(account):
    ships = get_list_or_404(Ship, account=account)

    civil_points = 0
    military_points = 0

    for s in ships:
        this_ship = s.as_real_class()
        this_ship_points = this_ship.count * (this_ship.cost[0] + this_ship.cost[1] + this_ship.cost[2])

        if s.content_type.model_class() in [Civil202, Civil203, Civil208, Civil210, Civil212]:
            civil_points += this_ship_points
        else:
            military_points += this_ship_points

    ship_points = civil_points + military_points

    return ship_points, civil_points, military_points


def get_research_points(account):
    research = get_list_or_404(Research, account=account)

    research_points = 0

    for r in research:
        this_research_cost = r.get_total_cost()
        research_points += this_research_cost[0] + this_research_cost[1] + this_research_cost[2]

    return research_points

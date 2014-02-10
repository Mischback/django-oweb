# Django imports
from django.shortcuts import get_list_or_404
# app imports
from oweb.models.building import Building, Supply1, Supply2, Supply3, Supply4, Supply12
from oweb.models.defense import Defense

def get_planet_points(planet_id):
    buildings = get_list_or_404(Building, planet=planet_id)
    defense = get_list_or_404(Defense, planet=planet_id)

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

    return (planet_points, production_points, other_points, defense_points)

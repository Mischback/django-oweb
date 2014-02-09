# Django imports
from django.shortcuts import get_list_or_404
# app imports
from oweb.models.building import Building, Supply1, Supply2, Supply3, Supply4, Supply12

def get_planet_points(planet_id):
    buildings = get_list_or_404(Building, planet=planet_id)

    building_points = 0
    other_points = 0
    production_points = 0

    for b in buildings:
        this_building_cost = b.get_total_cost()
        this_building_points = this_building_cost[0] + this_building_cost[1] + this_building_cost[2]

        if b.content_type.model_class() in [Supply1, Supply2, Supply3, Supply4, Supply12]:
            production_points += this_building_points
        else:
            other_points += this_building_points

        building_points += this_building_points

    planet_points = building_points

    return (planet_points, building_points, production_points, other_points)

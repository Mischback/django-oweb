"""
@file   building.py
@brief  Contains all building related classes
"""

# Django stuff
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Advisor stuff
from oweb.models import Planet
from oweb.libs.costs import costs_two, costs_two_total, costs_onepointfive, costs_onepointfive_total, costs_onepointsix, costs_onepointsix_total, costs_onepointeight, costs_onepointeight_total, costs_twopointthree, costs_twopointthree_total


class Building(models.Model):
    """
    @class  Building
    @brief  Base class for all buildings
    """

    """ @brief  meta variable to determine the "real" type of an instance """
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    """ @brief  The parent planet object """
    planet = models.ForeignKey(Planet)

    """ @brief  The name of the building """
    name = models.CharField(max_length=150)

    """ @brief  Current level of the building """
    level = models.IntegerField(default=0)

    """ @brief  The base costs of the building """
    base_cost = (0, 0, 0, 0)

    def get_next_cost(self):
        """
        @brief  Returns a tupel with the costs of the next level

        Please note, that the real calculation is done in the
        _calc_next_cost() function. This construct is necessary to access the
        "real" objects calculation function.
        """
        return self.as_real_class()._calc_next_cost()

    def get_total_cost(self):
        """
        @brief  Returns a tupel with the total costs of the current level

        Please note, that the real calculation is done in the
        _calc_total_cost() function. This construct is necessary to access the
        "real" objects calculation function.
        """
        return self.as_real_class()._calc_total_cost()

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_two(self.base_cost, self.level)

    def _calc_total_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_two_total(self.base_cost, self.level)

    def save(self, *args, **kwargs):
        """
        @brief  Overwrites the Models save()-method to store the "real" class
        """
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_real_class(self):
        """
        @brief  Access the "real" class methods
        """
        model = self.content_type.model_class()
        if model == Building:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        """
        @brief  Returns a string containing the name
        @retval STRING  A unicode string
        """
        return '{0}: {1}'.format(self.name, self.level)

    class Meta:
        app_label = 'oweb'


class Building_onepointfive(Building):
    """
    @class  Building_onepointfive
    @brief  Calculates the costs for buildings with a modfier of 1.5

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.5 and is suitable for:
    - Metallmine
    - Deuteriumsynthetisierer
    - Solarkraftwerk
    """

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointfive(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointfive_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_onepointsix(Building):
    """
    @class  Building_onepointsix
    @brief  Calculates the costs for buildings with a modfier of 1.5

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.6 and is suitable for:
    - Kristallmine
    """

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointsix(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointsix_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_onepointeight(Building):
    """
    @class  Building_onepointeight
    @brief  Calculates the costs for buildings with a modfier of 1.8

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.8 and is suitable for:
    - Fusionskraftwerk
    """

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointeight(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointeight_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_twopointthree(Building):
    """
    @class  Building_twopointthree
    @brief  Calculates the costs for buildings with a modfier of 2.3

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 2.3 and is suitable for:
    - Metallversteck
    - Kristallversteck
    - Deuteriumversteck
    """

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_twopointthree(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_twopointthree_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Supply1(Building_onepointfive):
    """
    @class  Supply1
    @brief  Building __Metallmine__
    """
    base_cost = (60, 15, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Metal Mine'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply2(Building_onepointsix):
    """
    @class  Supply2
    @brief  Building __Kristallmine__
    """
    base_cost = (48, 24, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Crystal Mine'
        Building_onepointsix.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply3(Building_onepointfive):
    """
    @class  Supply3
    @brief  Building __Deuteriumsynthetisierer__
    """
    base_cost = (225, 75, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deuterium Synthesizer'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply4(Building_onepointfive):
    """
    @class  Supply4
    @brief  Building __Solarkraftwerk__
    """
    base_cost = (75, 30, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Solar Plant'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply12(Building_onepointeight):
    """
    @class  Supply12
    @brief  Building __Fusionskraftwerk__
    """
    base_cost = (900, 360, 180, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Fusion Reactor'
        Building_onepointeight.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply22(Building):
    """
    @class  Supply22
    @brief  Building __Metallspeicher__
    """
    base_cost = (1000, 0, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Metal Storage'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply23(Building):
    """
    @class  Supply23
    @brief  Building __Kristallspeicher__
    """
    base_cost = (1000, 500, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Crystal Storage'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply24(Building):
    """
    @class  Supply24
    @brief  Building __Deuteriumtank__
    """
    base_cost = (1000, 1000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deuterium Tank'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply25(Building_twopointthree):
    """
    @class  Supply25
    @brief  Building __Metallversteck__
    """
    base_cost = (2645, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Shielded Metal Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply26(Building_twopointthree):
    """
    @class  Supply26
    @brief  Building __Kristallversteck__
    """
    base_cost = (2645, 1322, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Underground Crystal Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply27(Building_twopointthree):
    """
    @class  Supply27
    @brief  Building __Deuteriumversteck__
    """
    base_cost = (2645, 2645, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Seabed Deuterium Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station14(Building):
    """
    @class  Station14
    @brief  Building __Roboterfabrik__
    """
    base_cost = (400, 120, 200, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Robotics Factory'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station15(Building):
    """
    @class  Station15
    @brief  Building __Nanitenfabrik__
    """
    base_cost = (1000000, 500000, 100000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Nanite Factory'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station21(Building):
    """
    @class  Station21
    @brief  Building __Raumschiffwerft__
    """
    base_cost = (400, 200, 100)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Shipyard'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station31(Building):
    """
    @class  Station31
    @brief  Building __Forschungslabor__
    """
    base_cost = (200, 400, 200, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Research Lab'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station33(Building):
    """
    @class  Station33
    @brief  Building __Terraformer__
    """
    base_cost = (0, 50000, 100000, 1000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Terraformer'
        Building.__init__(self, *args, **kwargs)

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the building

        This building is the only one, which requires a certain amount of
        energy.

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.

        The formulas are taken from owiki.de
        """
        metal = self.base_cost[0] / 2 * 2 ** (self.level + 1)
        crystal = self.base_cost[1] / 2 * 2 ** (self.level + 1)
        deut = self.base_cost[2] / 2 * 2 ** (self.level + 1)
        energy = self.base_cost[3] / 2 * 2 ** (self.level + 1)
        return (int(metal), int(crystal), int(deut), int(energy))

    class Meta:
        app_label = 'oweb'


class Station34(Building):
    """
    @class  Station34
    @brief  Building __Allianzdepot__
    """
    base_cost = (20000, 40000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Alliance Depot'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station44(Building):
    """
    @class  Station44
    @brief  Building __Raketensilo__
    """
    base_cost = (20000, 20000, 1000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Missile Silo'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'

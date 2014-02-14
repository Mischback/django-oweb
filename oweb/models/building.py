"""This module contains all building related classes.

The module works this way: There is a base class for all buildings (:py:class:`Building`).
Several classes are directly derived from :py:class:`Building`: :py:class:`Building_onepointfive`,
:py:class:`Building_onepointsix`, :py:class:`Building_onepointeight` and
:py:class:`Building_twopointthree`.

These classes represent certain possibilities, how the costs of each level of a building may rise.
I.e. the :py:class:`Supply1` is derived from :py:class:`Building_onepointfive`, which means, 
that each level of a Metal Mine costs 1.5 * of the last costs.

The classes implement the function ``_calc_next_cost()`` with their respective modifier. This means, 
they are calling the right function from :py:mod:`oweb.libs.costs`.

The *real* building classes are derived from these classes. The classes, that are directly
derived from :py:class:`Building` have a cost modifier of 2.0. These *real* classes will also
set the correct ``base_cost`` of the building.
"""

# Django stuff
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Advisor stuff
from oweb.models.planet import AstronomicalObject
from oweb.libs.costs import costs_two, costs_two_total, costs_onepointfive, costs_onepointfive_total, costs_onepointsix, costs_onepointsix_total, costs_onepointeight, costs_onepointeight_total, costs_twopointthree, costs_twopointthree_total


class Building(models.Model):
    """Base class for all buildings"""

    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    """meta variable to determine the "real" type of an instance"""

    astro_object = models.ForeignKey(AstronomicalObject)
    """The parent planet or moon object """

    name = models.CharField(max_length=150)
    """The name of the building """

    level = models.IntegerField(default=0)
    """Current level of the building """

    base_cost = (0, 0, 0, 0)
    """The base costs of the building """

    def get_next_cost(self):
        """Returns a tupel with the costs of the next level

        Please note, that the real calculation is done in the
        _calc_next_cost() function. This construct is necessary to access the
        "real" objects calculation function.
        """
        return self.as_real_class()._calc_next_cost()

    def get_total_cost(self):
        """Returns a tupel with the total costs of the current level

        Please note, that the real calculation is done in the
        _calc_total_cost() function. This construct is necessary to access the
        "real" objects calculation function.
        """
        return self.as_real_class()._calc_total_cost()

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_two(self.base_cost, self.level)

    def _calc_total_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_two_total(self.base_cost, self.level)

    def save(self, *args, **kwargs):
        """Overwrites the Models save()-method to store the "real" class"""
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_real_class(self):
        """Access the "real" class methods"""
        model = self.content_type.model_class()
        if model == Building:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        return '{0}: {1}'.format(self.name, self.level)

    class Meta:
        app_label = 'oweb'


class Building_onepointfive(Building):
    """Calculates the costs for buildings with a modfier of 1.5

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.5 and is suitable for:
    - Metallmine
    - Deuteriumsynthetisierer
    - Solarkraftwerk
    """

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointfive(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointfive_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_onepointsix(Building):
    """Calculates the costs for buildings with a modfier of 1.5

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.6 and is suitable for:
    - Kristallmine
    """

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointsix(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointsix_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_onepointeight(Building):
    """Calculates the costs for buildings with a modfier of 1.8

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 1.8 and is suitable for:
    - Fusionskraftwerk
    """

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_onepointeight(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_onepointeight_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Building_twopointthree(Building):
    """Calculates the costs for buildings with a modfier of 2.3

    The base Building class uses a modifier of 2.0, which is suitable for most
    buildings.

    This class uses a modifier of 2.3 and is suitable for:
    - Metallversteck
    - Kristallversteck
    - Deuteriumversteck
    """

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This function should **not** be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.
        """
        return costs_twopointthree(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_twopointthree_total(self.base_cost, self.level)

    class Meta:
        proxy = True


class Supply1(Building_onepointfive):
    """Building **Metal Mine**"""
    base_cost = (60, 15, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Metal Mine'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply2(Building_onepointsix):
    """Building **Crystal Mine**"""
    base_cost = (48, 24, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Crystal Mine'
        Building_onepointsix.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply3(Building_onepointfive):
    """Building **Deuterium Synthesizer**"""
    base_cost = (225, 75, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deuterium Synthesizer'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply4(Building_onepointfive):
    """Building **Solar Plant**"""
    base_cost = (75, 30, 0, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Solar Plant'
        Building_onepointfive.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply12(Building_onepointeight):
    """Building **Fusion Reactor**"""
    base_cost = (900, 360, 180, 0)
    performance = models.FloatField(default=1.0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Fusion Reactor'
        Building_onepointeight.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply22(Building):
    """Building **Metal Storage**"""
    base_cost = (1000, 0, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Metal Storage'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply23(Building):
    """Building **Crystal Storage**"""
    base_cost = (1000, 500, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Crystal Storage'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply24(Building):
    """Building **Deuterium Tank**"""
    base_cost = (1000, 1000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deuterium Tank'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply25(Building_twopointthree):
    """Building **Shielded Metal Den**"""
    base_cost = (2645, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Shielded Metal Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply26(Building_twopointthree):
    """Building **Underground Crystal Den**"""
    base_cost = (2645, 1322, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Underground Crystal Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Supply27(Building_twopointthree):
    """Building **Seabed Deuterium Den**"""
    base_cost = (2645, 2645, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Seabed Deuterium Den'
        Building_twopointthree.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station14(Building):
    """Building **Robotics Factory**"""
    base_cost = (400, 120, 200, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Robotics Factory'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station15(Building):
    """Building **Nanite Factory**"""
    base_cost = (1000000, 500000, 100000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Nanite Factory'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station21(Building):
    """Building **Shipyard**"""
    base_cost = (400, 200, 100)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Shipyard'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station31(Building):
    """Building **Research Lab**"""
    base_cost = (200, 400, 200, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Research Lab'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station33(Building):
    """Building **Terraformer**"""
    base_cost = (0, 50000, 100000, 1000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Terraformer'
        Building.__init__(self, *args, **kwargs)

    def _calc_next_cost(self):
        """Calculates the cost of the next level of the building

        This building is the only one, which requires a certain amount of
        energy, therefore this method is implemented here.

        This function should **not** be called directly! Use get_next_cost()
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
    """Building **Alliace Depot**"""
    base_cost = (20000, 40000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Alliance Depot'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station41(Building):
    """Building **Lunar Base**"""
    base_cost = (20000, 40000, 20000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Lunar Base'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station42(Building):
    """Building **Sensor Phalanx**"""
    base_cost = (20000, 40000, 20000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Sensor Phalanx'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station43(Building):
    """Building **Jump Gate**"""
    base_cost = (2000000, 4000000, 2000000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Jump Gate'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Station44(Building):
    """Building **Missile Silo**"""
    base_cost = (20000, 20000, 1000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Missile Silo'
        Building.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'

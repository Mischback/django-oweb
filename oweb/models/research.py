# Python imports
from math import floor
# Django imports
from django.db import models
from django.contrib.contenttypes.models import ContentType
# app imports
from oweb.models import Account
from oweb.libs.costs import costs_two, costs_two_total, costs_total


class Research(models.Model):
    """
    @class  Research
    @brief  Base class for all researches
    """
    real_class = models.ForeignKey(ContentType, editable=False, null=True)
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100, default='Research')
    level = models.IntegerField(default=0)

    base_cost = (0, 0, 0, 0)

    def get_next_cost(self):
        """
        @brief  This function returns a tupel with the costs of the next level

        The tupel contains 4 values: Metal, Crystal, Deut and Energy.

        Please note, that the real calculation is done in the
        _calc_next_cost() function. This construct is necessary to access the
        "real" objects calculation function.
        """
        return self.as_real_class()._calc_next_cost()

    def get_total_cost(self):
        return self.as_real_class()._calc_total_cost()

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the research

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.

        The formulas are taken from owiki.de
        """
        return costs_two(self.base_cost, self.level)

    def _calc_total_cost(self):
        return costs_two_total(self.base_cost, self.level)

    def save(self, *args, **kwargs):
        """
        @brief  Overwrites the Models save()-method to store the "real" class
        """
        if (not self.real_class):
            self.real_class = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_real_class(self):
        """
        @brief  Access the "real" class methods
        """
        model = self.real_class.model_class()
        if model == Research:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        """
        @brief  Returns a string to identify the research
        """
        return '{0}: {1}'.format(self.name, self.level)

    class Meta:
        app_label = 'oweb'


class Research106(Research):
    """
    @class  Research106
    @brief  Research sibling for __Spionagetechnik__
    """
    base_cost = (200, 1000, 200, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Espionage Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research108(Research):
    """
    @class  Research108
    @brief  Research sibling for __Computertechnik__
    """
    base_cost = (0, 400, 600, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Computer Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research109(Research):
    """
    @class  Research109
    @brief  Research sibling for __Waffentechnik__
    """
    base_cost = (800, 200, 0, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Weapons Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research110(Research):
    """
    @class  Research110
    @brief  Research sibling for __Schildtechnik__
    """
    base_cost = (200, 600, 0, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Shielding Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research111(Research):
    """
    @class  Research111
    @brief  Research sibling for __Raumschiffpanzerung__
    """
    base_cost = (1000, 0, 0, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Armour Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research113(Research):
    """
    @class  Research113
    @brief  Research sibling for __Energietechnik__
    """
    base_cost = (0, 800, 400, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Energy Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research114(Research):
    """
    @class  Research114
    @brief  Research sibling for __Hyperraumtechnik__
    """
    base_cost = (0, 4000, 2000, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Hyperspace Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research115(Research):
    """
    @class  Research115
    @brief  Research sibling for __Verbrennungstriebwerk__
    """
    base_cost = (400, 0, 600, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Combustion Drive'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research117(Research):
    """
    @class  Research117
    @brief  Research sibling for __Impulstriebwerk__
    """
    base_cost = (2000, 4000, 600, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Impulse Drive'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research118(Research):
    """
    @class  Research118
    @brief  Research sibling for __Hyperraumantrieb__
    """
    base_cost = (10000, 20000, 6000, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Hyperspace Drive'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research120(Research):
    """
    @class  Research120
    @brief  Research sibling for __Lasertechnik__
    """
    base_cost = (200, 100, 0, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Laser Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research121(Research):
    """
    @class  Research121
    @brief  Research sibling for __Ionentechnik__
    """
    base_cost = (1000, 300, 100, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Ion Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research122(Research):
    """
    @class  Research122
    @brief  Research sibling for __Plasmatechnik__
    """
    base_cost = (2000, 4000, 1000, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Plasma Technology'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research123(Research):
    """
    @class  Research123
    @brief  Research sibling for __Intergalaktisches Forschungsnetzwerk__
    """
    base_cost = (240000, 400000, 160000, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Intergalactic Research Network'
        Research.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Research124(Research):
    """
    @class  Research124
    @brief  Research sibling for __Astrophysik__
    """
    base_cost = (4000, 8000, 4000, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Astrophysics'
        Research.__init__(self, *args, **kwargs)

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the research

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.

        The formulas are taken from owiki.de
        """
        metal = int(100 * (floor(0.5 + (self.base_cost[0] / 100) * 1.75 ** self.level)))
        crystal = int(100 * (floor(0.5 + (self.base_cost[1] / 100) * 1.75 ** self.level)))
        deut = int(100 * (floor(0.5 + (self.base_cost[2] / 100) * 1.75 ** self.level)))
        return (metal, crystal, deut, 0)

    def _calc_total_cost(self):
        return costs_total(self.base_cost, 1.75, self.level)

    class Meta:
        app_label = 'oweb'


class Research199(Research):
    """
    @class  Research124
    @brief  Research sibling for __Gravitonforschung__
    """
    base_cost = (0, 0, 0, 0)

    def __init__(self, *args, **kwargs):
        """
        @brief  Overwritten constructor to set the name
        """
        self._meta.get_field('name').default = 'Graviton Technology'
        Research.__init__(self, *args, **kwargs)

    def _calc_next_cost(self):
        """
        @brief  Calculates the cost of the next level of the research

        This function should __not__ be called directly! Use get_next_cost()
        instead, as it will make sure to call the correct calculation
        function.

        The formulas are taken from owiki.de
        """
        return (0, 0, 0, (100000 * 3 ** (self.level + 1)))

    class Meta:
        app_label = 'oweb'

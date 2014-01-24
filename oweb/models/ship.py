"""
@file   ship.py
@brief  Contains all ship related classes
"""

# Django stuff
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Advisor stuff
from oweb.models import Account, Planet


class Ship(models.Model):
    """
    @class  Ship
    @brief  Base class for all ships
    """

    """ @brief  meta variable to determine the "real" type of an instance """
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=150)
    count = models.IntegerField(default=0)
    cost = (0, 0, 0)

    def get_cost(self):
        return self.cost

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
        if model == Ship:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        """
        @brief  Returns a string containing the name
        @retval STRING  A unicode string
        """
        return '{0}: {1}'.format(self.name, self.count)

    class Meta:
        app_label = 'oweb'


class Military204(Ship):
    """
    @class  Military204
    @brief  __Leichter Jaeger__
    """
    cost = (3000, 1000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Light Fighter'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military205(Ship):
    """
    @class  Military205
    @brief  __Schwerer Jaeger__
    """
    cost = (6000, 4000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Heavy Figher'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military206(Ship):
    """
    @class  Military206
    @brief  __Kreuzer__
    """
    cost = (20000, 7000, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Cruiser'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military207(Ship):
    """
    @class  Military207
    @brief  __Schlachtschiff__
    """
    cost = (45000, 15000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Battleship'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military215(Ship):
    """
    @class  Military215
    @brief  __Schlachtkreuzer__
    """
    cost = (30000, 40000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Battlecruiser'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military211(Ship):
    """
    @class  Military211
    @brief  __Bomber__
    """
    cost = (50000, 25000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Bomber'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military213(Ship):
    """
    @class  Military213
    @brief  __Zerstoerer__
    """
    cost = (60000, 50000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Destroyer'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military214(Ship):
    """
    @class  Military214
    @brief  __Todesstern__
    """
    cost = (5000000, 4000000, 1000000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deathstar'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil202(Ship):
    """
    @class  Civil202
    @brief  __Kleiner Transporter__
    """
    cost = (2000, 2000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Small Cargo'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil203(Ship):
    """
    @class  Civil203
    @brief  __Grosser Transporter__
    """
    cost = (6000, 6000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Large Cargo'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil208(Ship):
    """
    @class  Civil208
    @brief  __Kolonieschiff__
    """
    cost = (10000, 20000, 10000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Colony Ship'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil209(Ship):
    """
    @class  Civil209
    @brief  __Recycler__
    """
    cost = (10000, 6000, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Recycler'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil210(Ship):
    """
    @class  Civil210
    @brief  __Spionagesonde__
    """
    cost = (1000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Espionage Probe'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil212(Ship):
    """
    @class  Civil210
    @brief  __Solarsatellit__
    """
    planet = models.ForeignKey(Planet)
    cost = (0, 2000, 500)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Solar Satellite'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'

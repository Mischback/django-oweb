"""Contains all ship related classes"""
# Django imports
from django.db import models
from django.contrib.contenttypes.models import ContentType
# app stuff
from oweb.models import Account, AstronomicalObject


class Ship(models.Model):
    """Base class for all ships"""

    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    """meta variable to determine the "real" type of an instance"""

    account = models.ForeignKey(Account)
    """A ForeignKey to the :py:class:`oweb.models.account.Account`"""

    name = models.CharField(max_length=150)
    """The name of this ship"""

    count = models.IntegerField(default=0)
    """How many of this ships are present"""

    cost = (0, 0, 0)
    """The costs per piece"""

    def get_cost(self):
        """Returns the cost of this device"""
        return self.cost

    def save(self, *args, **kwargs):
        """Overwrites the Models ``save()``-method to store the *real* class"""
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_real_class(self):
        """Access the *real* class methods"""
        model = self.content_type.model_class()
        if model == Ship:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        return '{0}: {1}'.format(self.name, self.count)

    class Meta:
        app_label = 'oweb'


class Military204(Ship):
    """Ship **Light Fighter**"""
    cost = (3000, 1000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Light Fighter'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military205(Ship):
    """Ship **Heavy Fighter**"""
    cost = (6000, 4000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Heavy Figher'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military206(Ship):
    """Ship **Cruiser**"""
    cost = (20000, 7000, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Cruiser'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military207(Ship):
    """Ship **Battleship**"""
    cost = (45000, 15000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Battleship'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military215(Ship):
    """Ship **Battlecruiser**"""
    cost = (30000, 40000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Battlecruiser'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military211(Ship):
    """Ship **Bomber**"""
    cost = (50000, 25000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Bomber'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military213(Ship):
    """Ship **Destroyer**"""
    cost = (60000, 50000, 15000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Destroyer'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Military214(Ship):
    """Ship **Deathstar**"""
    cost = (5000000, 4000000, 1000000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Deathstar'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil202(Ship):
    """Ship **Small Cargo**"""
    cost = (2000, 2000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Small Cargo'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil203(Ship):
    """Ship **Large Cargo**"""
    cost = (6000, 6000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Large Cargo'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil208(Ship):
    """Ship **Colony Ship**"""
    cost = (10000, 20000, 10000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Colony Ship'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil209(Ship):
    """Ship **Recycler**"""
    cost = (10000, 6000, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Recycler'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil210(Ship):
    """Ship **Espionage Probe**"""
    cost = (1000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Espionage Probe'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Civil212(Ship):
    """Ship **Solar Satellite**"""

    astro_object = models.ForeignKey(AstronomicalObject)
    """Reference to the planet"""

    cost = (0, 2000, 500)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Solar Satellite'
        Ship.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'

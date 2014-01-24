"""
@file   defense.py
@brief  Contains all defense related classes
"""

# Django stuff
from django.db import models
from django.contrib.contenttypes.models import ContentType

# Advisor stuff
from oweb.models import Planet


class Defense(models.Model):

    """ @brief  meta variable to determine the "real" type of an instance """
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    """ @brief  The parent planet object """
    planet = models.ForeignKey(Planet)

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
        if model == Defense:
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


class Defense401(Defense):
    cost = (2000, 0, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Rocket Launcher'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense402(Defense):
    cost = (1500, 500, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Light Laser'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense403(Defense):
    cost = (6000, 2000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Heavy Laser'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense404(Defense):
    cost = (20000, 15000, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Gauss Cannon'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense405(Defense):
    cost = (2000, 6000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Ion Cannon'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense406(Defense):
    cost = (50000, 50000, 30000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Plasma Turret'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense407(Defense):
    cost = (10000, 10000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Small Shield Dome'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense408(Defense):
    cost = (50000, 50000, 0)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Large Shield Dome'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense502(Defense):
    cost = (8000, 0, 2000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Anti-Ballistic Missiles'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'


class Defense503(Defense):
    cost = (12500, 2500, 10000)

    def __init__(self, *args, **kwargs):
        self._meta.get_field('name').default = 'Interplanetary Missiles'
        Defense.__init__(self, *args, **kwargs)

    class Meta:
        app_label = 'oweb'

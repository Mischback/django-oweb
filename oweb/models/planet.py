# Django imports
from django.db import models
from django.contrib.contenttypes.models import ContentType
# app imports
from oweb.models import Account

class AstronomicalObject(models.Model):

    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    """meta variable to determine the "real" type of an instance"""
    name = models.CharField(max_length=100, default='Colony')
    """The name of this planet"""
    coord = models.CharField(max_length=15, default='0:000:00')
    """The coordinates of this planet"""

    def save(self, *args, **kwargs):
        """Overwrites the Models save()-method to store the "real" class"""
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        self.save_base()

    def as_real_class(self):
        """Access the "real" class methods"""
        model = self.content_type.model_class()
        if model == AstronomicalObject:
            return self
        return model.objects.get(id=self.id)

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        app_label = 'oweb'


class Planet(AstronomicalObject):
    """Represents a planet"""

    account = models.ForeignKey(Account)
    """A ForeignKey to the :py:class:`oweb.models.account.Account`"""
    max_temp = models.IntegerField(default=0)
    """The minimal temperature of this planet"""

    def __unicode__(self):
        return '{0} [{1}]'.format(self.name, self.coord)

    class Meta:
        app_label = 'oweb'


class Moon(AstronomicalObject):
    """Represents a moon"""

    planet = models.ForeignKey(Planet)
    """A ForeignKey to the :py:class:`oweb.models.planet.Planet`"""

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        app_label = 'oweb'

# Django imports
from django.db import models
# app imports
from oweb.models import Account

class Planet(models.Model):
    """Represents a planet"""

    account = models.ForeignKey(Account)
    """A ForeignKey to the :py:class:`oweb.models.account.Account`"""

    name = models.CharField(max_length=100, default='Colony')
    """The name of this planet"""

    coord = models.CharField(max_length=15, default='0:000:00')
    """The coordinates of this planet"""

    min_temp = models.IntegerField(default=0)
    """The minimal temperature of this planet"""

    def __unicode__(self):
        return '{0} [{1}]'.format(self.name, self.coord)

    class Meta:
        app_label = 'oweb'


class Moon(models.Model):
    """Represents a moon"""

    planet = models.ForeignKey(Planet)
    """A ForeignKey to the :py:class:`oweb.models.planet.Planet`"""

    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        app_label = 'oweb'

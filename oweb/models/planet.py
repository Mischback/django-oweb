# Django imports
from django.db import models
# app imports
from oweb.models import Account

class Planet(models.Model):
    """
    @class  Planet
    @brief  Represents a planet
    """
    account = models.ForeignKey(Account)
    name = models.CharField(max_length=100, default='Colony')
    coord = models.CharField(max_length=15, default='0:000:00')
    min_temp = models.IntegerField(default=0)

    def __unicode__(self):
        return '{0} [{1}]'.format(self.name, self.coord)

    class Meta:
        app_label = 'oweb'

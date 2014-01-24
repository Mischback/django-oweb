# Django imports
from django.conf import settings
from django.db import models


class Account(models.Model):
    """
    @class  Account
    @brief  Represents a OGame account
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    universe = models.CharField(max_length=100, default='no universe specified')
    username = models.CharField(max_length=100, default='no username specified')
    speed = models.IntegerField(default=1)
    trade_metal = models.IntegerField(default=3)
    trade_crystal = models.IntegerField(default=2)
    trade_deut = models.IntegerField(default=1)

    def __unicode__(self):
        return 'Account {0} ({1})'.format(self.username, self.universe)

    class Meta:
        app_label = 'oweb'

"""This module includes all account related stuff"""
# Django imports
from django.conf import settings
from django.db import models


class Account(models.Model):
    """Represents an OGame Account
    
    An Account object is the root for all data. An Account is associated with 
    a Django User (``owner``).

    The object stores general information, like the universe's name and speed, 
    the username and the trading rates, that are used for calculations.
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    """A Django User object to which this account is associated"""

    universe = models.CharField(max_length=100, default='no universe specified')
    """The name of this OGame universe"""

    username = models.CharField(max_length=100, default='no username specified')
    """The username of this OGame account"""

    speed = models.IntegerField(default=1)
    """The speed of this OGame universe
    :type speed: int"""

    trade_metal = models.IntegerField(default=3)
    """The trading rate for metal
    
    Of couse, this is no *rate* by itsself. The trading rate is calculated in
    combination with ``trade_crystal`` and ``trade_deut``"""

    trade_crystal = models.IntegerField(default=2)
    """The trading rate for crystal
    
    Of couse, this is no *rate* by itsself. The trading rate is calculated in
    combination with ``trade_metal`` and ``trade_deut``"""

    trade_deut = models.IntegerField(default=1)
    """The trading rate for deuterium
    
    Of couse, this is no *rate* by itsself. The trading rate is calculated in
    combination with ``trade_metal`` and ``trade_crystal``"""


    def __unicode__(self):
        return 'Account {0} ({1})'.format(self.username, self.universe)

    class Meta:
        app_label = 'oweb'

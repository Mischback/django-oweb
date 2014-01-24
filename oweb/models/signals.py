# Django imports
from django.db.models import signals
# app imports
from oweb.models import Account, Planet
from oweb.models.research import *
from oweb.models.ship import *

def callback_create_account(sender, instance, created, **kwargs):
    """
    """
    if created:
        Research106.objects.create(account=instance)
        Research108.objects.create(account=instance)
        Research109.objects.create(account=instance)
        Research110.objects.create(account=instance)
        Research111.objects.create(account=instance)
        Research113.objects.create(account=instance)
        Research114.objects.create(account=instance)
        Research115.objects.create(account=instance)
        Research117.objects.create(account=instance)
        Research118.objects.create(account=instance)
        Research120.objects.create(account=instance)
        Research121.objects.create(account=instance)
        Research122.objects.create(account=instance)
        Research123.objects.create(account=instance)
        Research124.objects.create(account=instance)
        Research199.objects.create(account=instance)

        Military204.objects.create(account=instance)
        Military205.objects.create(account=instance)
        Military206.objects.create(account=instance)
        Military207.objects.create(account=instance)
        Military215.objects.create(account=instance)
        Military211.objects.create(account=instance)
        Military213.objects.create(account=instance)
        Military214.objects.create(account=instance)
        Civil202.objects.create(account=instance)
        Civil203.objects.create(account=instance)
        Civil208.objects.create(account=instance)
        Civil209.objects.create(account=instance)
        Civil210.objects.create(account=instance)

        Planet.objects.create(account=instance, name='Homeworld')


def callback_create_planet(sender, instance, created, **kwargs):
    """
    @brief  Callback function to be executed after Planet creation

    Basically this function adds buildings to the planet
    """
    if created:
        Supply1.objects.create(planet=instance)
        Supply2.objects.create(planet=instance)
        Supply3.objects.create(planet=instance)
        Supply4.objects.create(planet=instance)
        Supply12.objects.create(planet=instance)
        Supply22.objects.create(planet=instance)
        Supply23.objects.create(planet=instance)
        Supply24.objects.create(planet=instance)
        Supply25.objects.create(planet=instance)
        Supply26.objects.create(planet=instance)
        Supply27.objects.create(planet=instance)
        Station14.objects.create(planet=instance)
        Station15.objects.create(planet=instance)
        Station21.objects.create(planet=instance)
        Station31.objects.create(planet=instance)
        Station33.objects.create(planet=instance)
        Station34.objects.create(planet=instance)
        Station44.objects.create(planet=instance)

        Civil212.objects.create(account=instance.account, planet=instance)

        Defense401.objects.create(planet=instance)
        Defense402.objects.create(planet=instance)
        Defense403.objects.create(planet=instance)
        Defense404.objects.create(planet=instance)
        Defense405.objects.create(planet=instance)
        Defense406.objects.create(planet=instance)
        Defense407.objects.create(planet=instance)
        Defense408.objects.create(planet=instance)
        Defense502.objects.create(planet=instance)
        Defense503.objects.create(planet=instance)


# Register the callbacks
signals.post_save.connect(callback_create_account,
    sender=Account,
    weak=False,
    dispatch_uid='models.callback_create_account')

signals.post_save.connect(callback_create_planet,
    sender=Planet,
    weak=False,
    dispatch_uid='models.callback_create_planet')

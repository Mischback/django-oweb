# Django imports
from django.db.models import signals
# app imports
from oweb.models import Account, Planet, Moon
from oweb.models.research import *
from oweb.models.ship import *
from oweb.models.building import *
from oweb.models.defense import *

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
        Supply1.objects.create(astro_object=instance)
        Supply2.objects.create(astro_object=instance)
        Supply3.objects.create(astro_object=instance)
        Supply4.objects.create(astro_object=instance)
        Supply12.objects.create(astro_object=instance)
        Supply22.objects.create(astro_object=instance)
        Supply23.objects.create(astro_object=instance)
        Supply24.objects.create(astro_object=instance)
        Supply25.objects.create(astro_object=instance)
        Supply26.objects.create(astro_object=instance)
        Supply27.objects.create(astro_object=instance)
        Station14.objects.create(astro_object=instance)
        Station15.objects.create(astro_object=instance)
        Station21.objects.create(astro_object=instance)
        Station31.objects.create(astro_object=instance)
        Station33.objects.create(astro_object=instance)
        Station34.objects.create(astro_object=instance)
        Station44.objects.create(astro_object=instance)

        Civil212.objects.create(account=instance.account, astro_object=instance)

        Defense401.objects.create(astro_object=instance)
        Defense402.objects.create(astro_object=instance)
        Defense403.objects.create(astro_object=instance)
        Defense404.objects.create(astro_object=instance)
        Defense405.objects.create(astro_object=instance)
        Defense406.objects.create(astro_object=instance)
        Defense407.objects.create(astro_object=instance)
        Defense408.objects.create(astro_object=instance)
        Defense502.objects.create(astro_object=instance)
        Defense503.objects.create(astro_object=instance)


def callback_create_moon(sender, instance, created, **kwargs):
    if created:
        Supply22.objects.create(astro_object=instance)
        Supply23.objects.create(astro_object=instance)
        Supply24.objects.create(astro_object=instance)
        Supply25.objects.create(astro_object=instance)
        Supply26.objects.create(astro_object=instance)
        Supply27.objects.create(astro_object=instance)
        Station14.objects.create(astro_object=instance)
        Station21.objects.create(astro_object=instance)
        Station41.objects.create(astro_object=instance)
        Station42.objects.create(astro_object=instance)
        Station43.objects.create(astro_object=instance)

        Civil212.objects.create(account=instance.planet.account, astro_object=instance)

        Defense401.objects.create(astro_object=instance)
        Defense402.objects.create(astro_object=instance)
        Defense403.objects.create(astro_object=instance)
        Defense404.objects.create(astro_object=instance)
        Defense405.objects.create(astro_object=instance)
        Defense406.objects.create(astro_object=instance)
        Defense407.objects.create(astro_object=instance)
        Defense408.objects.create(astro_object=instance)
        Defense502.objects.create(astro_object=instance)
        Defense503.objects.create(astro_object=instance)


# Register the callbacks
signals.post_save.connect(callback_create_account,
    sender=Account,
    weak=False,
    dispatch_uid='models.callback_create_account')

signals.post_save.connect(callback_create_planet,
    sender=Planet,
    weak=False,
    dispatch_uid='models.callback_create_planet')

signals.post_save.connect(callback_create_moon,
    sender=Moon,
    weak=False,
    dispatch_uid='models.callback_create_moon')

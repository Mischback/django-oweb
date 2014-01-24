# Django imports
from django.db.models import signals
# app imports
from oweb.models import Account, Planet
from oweb.models.research import *

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

        Planet.objects.create(account=instance, name='Homeworld')

signals.post_save.connect(callback_create_account, 
    sender=Account,
    weak=False,
    dispatch_uid='models.callback_create_account')

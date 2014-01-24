# Django imports
from django.db.models import signals
# app imports
from oweb.models import Account, Planet

def callback_create_account(sender, instance, created, **kwargs):
    """
    """
    if created:
        Planet.objects.create(account=instance, name='Homeworld')

signals.post_save.connect(callback_create_account, 
    sender=Account,
    weak=False,
    dispatch_uid='models.callback_create_account')

"""Contains all views, that actually alters the database"""
# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
# app imports
from oweb.exceptions import OWebDoesNotExist, OWebAccountAccessViolation, OWebParameterMissingException, OWebIllegalParameterException
from oweb.models import Account, Building, Defense, Planet, Research, Ship, Moon
from oweb.libs.shortcuts import get_object_or_404


def item_update(req):
    """Generic function to update items

    Items are :py:class:`Building`, :py:class:`Research`, :py:class:`Ship`
    and :py:class:`Defense`"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    try:
        item_type = req.POST['item_type']
        item_id = req.POST['item_id']
        item_level = req.POST['item_level']
    except KeyError:
        raise OWebParameterMissingException

    if 'research' == item_type:
        obj = Research.objects.get(pk=item_id)
        account = obj.account
    elif 'ship' == item_type:
        obj = Ship.objects.get(pk=item_id)
        account = obj.account
    elif 'building' == item_type:
        obj = Building.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    elif 'moon_building' == item_type:
        obj = Building.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().planet.account
    elif 'defense' == item_type:
        obj = Defense.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().account
    elif 'moon_defense' == item_type:
        obj = Defense.objects.get(pk=item_id)
        account = obj.astro_object.as_real_class().planet.account
    else:
        raise OWebIllegalParameterException

    # check, if the objects account is actually owned by the current user
    if not req.user.id == account.owner_id:
        raise OWebAccountAccessViolation

    if not int(item_level) < 0:
        if isinstance(obj, Ship) or isinstance(obj, Defense):
            obj.count = item_level
        else:
            obj.level = item_level
        obj.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])

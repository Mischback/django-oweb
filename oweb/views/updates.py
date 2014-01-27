# Django imports
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
# app imports
from oweb.models import Research, Ship

def item_update(req):
    """
    """
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    try:
        item_type = req.POST['item_type']
        item_id = req.POST['item_id']
        item_level = req.POST['item_level']
    except:
        raise Http404

    if 'research' == item_type:
        obj = Research.objects.select_related('account').get(pk=item_id)
        account = obj.account
    elif 'ship' == item_type:
        obj = Ship.objects.select_related('account').get(pk=item_id)
        account = obj.account
    else:
        raise Http404

    # check, if the objects account is actually owned by the current user
    if not req.user.id == account.owner_id:
        raise Http404

    if not int(item_level) < 0:
        if isinstance(obj, Ship):
            obj.count = item_level
        else:
            obj.level = item_level
        obj.save()

    return HttpResponseRedirect(req.META['HTTP_REFERER'])

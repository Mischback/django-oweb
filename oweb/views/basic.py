# Django imports
from django.shortcuts import get_list_or_404, render
# app imports
from oweb.models import Account

def home(req):
    """todo Documentation still missing!"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # get all accounts of this user
    accounts = get_list_or_404(Account, owner_id=req.user.id)
    # render the template
    return render(req, 'oweb/home.html', 
        {'accounts': accounts}
    )
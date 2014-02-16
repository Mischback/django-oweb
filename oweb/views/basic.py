"""Contains general views"""
# Django imports
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
# app imports
from oweb.models import Account

def home(req):
    """Provides the home view"""
    # this is the non-decorator version of the login_required decorator
    # basically it checks, if the user is authenticated and redirects him, if
    # not. The decorator could not handle the reverse url-resolution.
    if not req.user.is_authenticated():
        return redirect(reverse('oweb:app_login'))

    # get all accounts of this user
    accounts = Account.objects.filter(owner_id=req.user.id)

    # render the template
    return render(req, 'oweb/home.html', 
        {'accounts': accounts}
    )

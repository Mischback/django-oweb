"""Contains tests for oweb.views.updates.create_account"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests
from oweb.models.account import Account


class OWebViewsCreateAccountTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:create_account'))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_redirect(self):
        """Does ``create_account()`` redirect to the correct page?"""
        accs = Account.objects.all()
        num_accs = len(accs) + 1
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:create_account'))
        self.assertRedirects(r,
                             reverse('oweb:account_settings', args=[num_accs]),
                             status_code=302,
                             target_status_code=200)

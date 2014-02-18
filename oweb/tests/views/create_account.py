"""Contains tests for oweb.views.updates.create_account"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsCreateAccountTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:item_update'))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``create_account()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_settings of new account)
        self.assertEqual(True, True)

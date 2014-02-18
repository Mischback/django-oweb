"""Contains tests for oweb.views.basic.home"""
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsHomeTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:home'))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_listing(self):
        """Does the home view list the correct accounts?"""
        # TODO insert real test here
        self.assertEqual(True, True)

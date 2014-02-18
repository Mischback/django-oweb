"""Contains tests for oweb.views.updates.item_update"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsPlanetCreateTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:planet_create', args=[1,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    @skip('not yet implemented')
    def test_account_owner(self):
        """Can somebody update an item he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``planet_create()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings of new planet)
        self.assertEqual(True, True)

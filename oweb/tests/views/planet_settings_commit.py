"""Contains tests for oweb.views.updates.item_update"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsPlanetSettingsCommitTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:planet_settings_update', args=[1,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_owner(self):
        """Can somebody update a planet he doesn't posess?"""
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:planet_settings_update', args=[1,]))
        self.assertEqual(r.status_code, 404)

    @skip('not yet implemented')
    def test_no_post(self):
        """What does ``planet_settings_commit()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``planet_settings_commit()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings)
        self.assertEqual(True, True)

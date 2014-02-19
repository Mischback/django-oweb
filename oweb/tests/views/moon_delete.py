"""Contains tests for oweb.views.updates.moon_delete"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsMoonDeleteTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:moon_delete', args=[3,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    @skip('not yet implemented')
    def test_account_owner(self):
        """Can somebody delete a moon in an account he doesn't posess?"""
        self.client.login(username='test02', password='foo')
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:moon_delete', args=[3,]))
        self.assertEqual(r.status_code, 404)
        r = self.client.post(reverse('oweb:moon_delete', args=[3,]))
        self.assertEqual(r.status_code, 404)

    @skip('not yet implemented')
    def test_get(self):
        """Does a GET to ``moon_delete()`` show the confirmation template?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``moon_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

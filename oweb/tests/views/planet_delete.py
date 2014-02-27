"""Contains tests for oweb.views.updates.planet_delete"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import User
# app imports
from oweb.tests import OWebViewTests
from oweb.models.account import Account
from oweb.models.planet import Planet


@override_settings(AUTH_USER_MODEL='auth.User')
class OWebViewsPlanetDeleteTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        acc = Account.objects.filter().first()
        p = Planet.objects.filter(account=acc).first()
        r = self.client.get(reverse('oweb:planet_delete', args=[acc.id, p.id]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    @skip('not yet implemented')
    def test_account_owner(self):
        """Can somebody delete a planet for an account he doesn't posess?"""
        self.client.login(username='test02', password='foo')
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:planet_delete', args=[1, 1,]))
        self.assertEqual(r.status_code, 404)
        r = self.client.post(reverse('oweb:planet_delete', args=[1, 1,]))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_planet_delete_get(self):
        """Does a GET to ``planet_delete()`` show the confirmation template?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_planet_delete_redirect(self):
        """Does ``planet_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_overview)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_planet_delete_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

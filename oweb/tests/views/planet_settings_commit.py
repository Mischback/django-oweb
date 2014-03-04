"""Contains tests for oweb.views.updates.planet_settings_commit"""
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
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        p = Planet.objects.filter(account=acc).first()
        self.client.login(username='test02', password='foo')
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:planet_settings_update', args=[p.id]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    def test_no_post_data(self):
        """What does ``planet_settings_commit()`` do, if no POST data is provided?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        p = Planet.objects.filter(account=acc).first()
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:planet_settings_update', args=[p.id]))
        self.assertEqual(r.status_code, 500)
        self.assertTemplateUsed(r, 'oweb/500.html')

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

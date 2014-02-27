"""Contains tests for oweb.views.updates.planet_create"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import User
# app imports
from oweb.tests import OWebViewTests
from oweb.models.account import Account


@override_settings(AUTH_USER_MODEL='auth.User')
class OWebViewsPlanetCreateTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:planet_create', args=[1,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_owner(self):
        """Can somebody create a planet in an account he doesn't posess?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        self.client.login(username='test02', password='foo')
        r = self.client.get(reverse('oweb:planet_create', args=[acc.id]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``planet_create()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings of new planet)
        self.assertEqual(True, True)

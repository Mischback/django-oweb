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

    def test_account_owner(self):
        """Can somebody delete a planet for an account he doesn't posess?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        p = Planet.objects.filter(account=acc).first()
        self.client.login(username='test02', password='foo')
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:planet_delete', args=[acc.id, p.id]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    def test_get(self):
        """Does a GET to ``planet_delete()`` show the confirmation template?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        p = Planet.objects.filter(account=acc).first()
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:planet_delete', args=[acc.id, p.id]))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'oweb/planet_delete.html')

    def test_redirect(self):
        """Does ``planet_delete()`` redirect to the correct page?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        p = Planet.objects.filter(account=acc).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:planet_delete', args=[acc.id, p.id]),
                             data={'confirm_planet_deletion': 'confirm'})
        self.assertRedirects(r,
                             reverse('oweb:account_overview', args=[acc.id]),
                             status_code=302,
                             target_status_code=200)

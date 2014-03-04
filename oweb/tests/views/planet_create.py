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
from oweb.models.planet import Planet


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

    def test_redirect(self):
        """Does ``planet_create()`` redirect to the correct page?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.filter(owner=u).first()
        planet_pre = set(Planet.objects.filter(account=acc).values_list('id', flat=True))
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:planet_create', args=[acc.id]))
        planet_post = set(Planet.objects.filter(account=acc).values_list('id', flat=True))
        new_p = list(planet_post - planet_pre)[0]
        self.assertRedirects(r,
                             reverse('oweb:planet_settings', args=[new_p]),
                             status_code=302,
                             target_status_code=200)

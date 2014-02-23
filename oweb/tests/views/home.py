"""Contains tests for oweb.views.basic.home"""
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
        u = User.objects.get(username='test01')
        accs = Account.objects.filter(owner=u)
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:home'))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'oweb/home.html')
        self.assertTrue('accounts' in r.context)
        self.assertEqual([acc.pk for acc in r.context['accounts']], [acc.pk for acc in accs])

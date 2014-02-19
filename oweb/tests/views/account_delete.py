"""Contains tests for oweb.views.updates.account_delete"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsAccountDeleteTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:account_delete', args=[1,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_owner(self):
        """Can somebody delete an account he doesn't posess?"""
        self.client.login(username='test02', password='foo')
        # Should display a 403-page and use oweb/403.html
        r = self.client.get(reverse('oweb:account_delete', args=[1,]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')
        r = self.client.post(reverse('oweb:account_delete', args=[1,]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    def test_get(self):
        """Does a GET to ``account_delete()`` show the confirmation template?"""
        self.client.login(username='test01', password='foo')
        # Should display oweb/account_delete.html with status 200
        r = self.client.get(reverse('oweb:account_delete', args=[1,]))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'oweb/account_delete.html')

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``planet_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to home)
        self.assertEqual(True, True)

    @skip('not yet implemented')
    def test_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

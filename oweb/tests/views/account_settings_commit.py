"""Contains tests for oweb.views.updates.account_settings_commit"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsAccountSettingsCommitTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:account_settings_commit', args=[1,]))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_owner(self):
        """Can somebody update an account he doesn't posess?"""
        self.client.login(username='test02', password='foo')
        # it is not required to test get and post, because both are handled in
        # the same way (regarding this scenario)
        r = self.client.get(reverse('oweb:account_settings_commit', args=[1,]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    def test_unknown_account(self):
        """What happens, if an invalid account_id is provided?"""
        self.client.login(username='test01', password='foo')
        r = self.client.get(reverse('oweb:account_settings_commit', args=[1338,]))
        self.assertEqual(r.status_code, 404)
        self.assertTemplateUsed(r, 'oweb/404.html')

    def test_no_post_data(self):
        """What does ``account_settings_commit()`` do, if no POST data is provided?"""
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:account_settings_commit', args=[1,]))
        self.assertEqual(r.status_code, 500)
        self.assertTemplateUsed(r, 'oweb/500.html')

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``account_settings_commit()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_settings)
        self.assertEqual(True, True)

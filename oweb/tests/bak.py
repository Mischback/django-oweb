# Django imports
from django.core.urlresolvers import reverse
from oweb.tests import OWebViewTests


class OWebViewLoginRequiredTests(OWebViewTests):
    """Tests for the required login
    
    Most views do require a login, but because of certain conditions, 
    the Django decorator is not used by this app. Therefore test cases for
    this implementations are provided.
    """

    def test_moon_create(self):
        r = self.client.get(reverse('oweb:moon_create', args=[1,]))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

    def test_moon_settings_commit(self):
        r = self.client.get(reverse('oweb:moon_settings_commit', args=[3,]))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

    def test_moon_delete(self):
        r = self.client.get(reverse('oweb:moon_delete', args=[3,]))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)


class OWebViewAccountOwnerTests(OWebViewTests):
    """Tests if the account owner is checked"""
    def setUp(self):
        # prepare a client login
        self.client.login(username='test02', password='foo')

    def test_moon_create(self):
        """Can somebody create a moon in an account he doesn't posess?"""
        r = self.client.get(reverse('oweb:moon_create', args=[1,]))
        self.assertEqual(r.status_code, 404)

    def test_moon_settings_commit(self):
        """Can somebody update a moon in an account he doesn't posess?"""
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:moon_settings_commit', args=[3,]))
        self.assertEqual(r.status_code, 404)
        r = self.client.post(reverse('oweb:moon_settings_commit', args=[3,]))
        self.assertEqual(r.status_code, 404)

    def test_moon_delete(self):
        """Can somebody delete a moon in an account he doesn't posess?"""
        # no need to perform a real POST request here, since the check is
        # performed before actual POST-parameters are considered
        r = self.client.get(reverse('oweb:moon_delete', args=[3,]))
        self.assertEqual(r.status_code, 404)
        r = self.client.post(reverse('oweb:moon_delete', args=[3,]))
        self.assertEqual(r.status_code, 404)


class OWebViewUpdatesTests(OWebViewTests):
    """Tests for views in views/updates.py"""

    def test_moon_create_redirect(self):
        """Does ``moon_create()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to moon_settings of new moon)
        self.assertEqual(True, True)

    def test_moon_settings_commit_no_post(self):
        """What does ``moon_settings_commit()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_moon_settings_commit_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_moon_settings_commit_redirect(self):
        """Does ``moon_settings_commit()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings)
        self.assertEqual(True, True)

    def test_moon_delete_get(self):
        """Does a GET to ``moon_delete()`` show the confirmation template?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_moon_delete_redirect(self):
        """Does ``moon_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet)
        self.assertEqual(True, True)

    def test_moon_delete_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

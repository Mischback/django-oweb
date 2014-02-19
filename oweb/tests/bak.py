class OWebViewAccountOwnerTests(OWebViewTests):
    """Tests if the account owner is checked"""
    def setUp(self):
        # prepare a client login
        self.client.login(username='test02', password='foo')

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


# Django imports
from django.test import TestCase
from django.core.urlresolvers import reverse

class OWebViewTests(TestCase):
    """Provides view related tests"""

    def test_home2login(self):
        """Redirect from home to login for unauthenticated users"""
        r = self.client.get(reverse('oweb:home'))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

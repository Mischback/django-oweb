# Django imports
from django.test import TestCase


class OWebViewTests(TestCase):
    """Provides view related tests"""
    fixtures = ['oweb_testdata_01.json']

    def setup(self):
        """Prepare general testing settings"""
        # urls must be specified this way, because the class-attribute can not
        # use a namespace, which is required by the app
        self.urls = patterns('',
            url(r'', include('oweb.urls', namespace='oweb')),
        )

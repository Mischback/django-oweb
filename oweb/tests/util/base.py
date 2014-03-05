"""Contains base classes for tests"""

# Django imports
from django.test import TestCase


class OWebTestBase(TestCase):
    """Base class for all tests of this app"""
    urls = 'oweb.tests.util.urls'
    fixtures = ['oweb_testdata_01.json']

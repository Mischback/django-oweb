# Django imports
from django.test import TestCase
from django.core.urlresolvers import reverse

class OWebViewTests(TestCase):
    """Provides view related tests"""
    pass


class OWebViewLoginRequiredTests(OWebViewTests):
    """Tests for the required login
    
    Most views do require a login, but because of certain conditions, 
    the Django decorator is not used by this app. Therefore test cases for
    this implementations are provided.
    """

    def test_home(self):
        r = self.client.get(reverse('oweb:home'))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

    def test_update(self):
        r = self.client.get(reverse('oweb:item_update'))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

    def test_create_account(self):
        r = self.client.get(reverse('oweb:create_account'))
        self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)

    def test_account_settings_commit(self):
        # TODO Needs data fixture, because it needs a valid account_id for reverse
        # r = self.client.get(reverse('oweb:accunt_settings_commit'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)


class OWebViewAccountOwnerTests(OWebViewTests):
    """Tests if the account owner is checked"""

    def test_update(self):
        """Can somebody update an item he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_account_settings_commit(self):
        """Can somebody update an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)


class OWebViewBasicTests(OWebViewTests):
    """Tests for views in views/basic.py"""

    def test_home_listing(self):
        """Does the home view list the correct accounts?"""
        # TODO insert real test here
        self.assertEqual(True, True)


class OWebViewUpdatesTests(OWebViewTests):
    """Tests for views in views/updates.py"""

    def test_update_no_post(self):
        """What does ``item_update()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_update_redirect(self):
        """Does ``item_update()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to referer)
        self.assertEqual(True, True)

    def test_update_research_update(self):
        """Does ``item_update()`` correctly update researches?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_ship_update(self):
        """Does ``item_update()`` correctly update ships?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_building_update(self):
        """Does ``item_update()`` correctly update buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_moon_building_update(self):
        """Does ``item_update()`` correctly update moon buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_defense_update(self):
        """Does ``item_update()`` correctly update defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_moon_defense_update(self):
        """Does ``item_update()`` correctly update moon defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_update_unknown_item_type(self):
        """Does ``item_update()`` correctly handle unknown item_types?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_update_create_account_redirect(self):
        """Does ``create_account()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_settings)
        self.assertEqual(True, True)

    def test_account_settings_commit_no_post(self):
        """What does ``account_settings_commit()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

# Django imports
from django.core.urlresolvers import reverse
from oweb.tests import OWebViewTests


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
        # r = self.client.get(reverse('oweb:account_settings_commit'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_planet_settings_commit(self):
        # TODO Needs data fixture, because it needs a valid planet_id for reverse
        # r = self.client.get(reverse('oweb:planet_settings_update'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_planet_create(self):
        # TODO Needs data fixture, because it needs a valid account_id for reverse
        # r = self.client.get(reverse('oweb:planet_create'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_planet_delete(self):
        # TODO Needs data fixture, because it needs a valid account_id and planet_id for reverse
        # r = self.client.get(reverse('oweb:planet_delete'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_account_delete(self):
        # TODO Needs data fixture, because it needs a valid account_id for reverse
        # r = self.client.get(reverse('oweb:account_delete'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_moon_create(self):
        # TODO Needs data fixture, because it needs a valid planet_id for reverse
        # r = self.client.get(reverse('oweb:moon_create'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_moon_settings_commit(self):
        # TODO Needs data fixture, because it needs a valid moon_id for reverse
        # r = self.client.get(reverse('oweb:moon_settings_update'))
        # self.assertRedirects(r, reverse('oweb:app_login'), status_code=302, target_status_code=200)
        self.assertEqual(True, True)

    def test_moon_delete(self):
        # TODO Needs data fixture, because it needs a valid moon_id for reverse
        # r = self.client.get(reverse('oweb:moon_delete'))
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

    def test_planet_settings_commit(self):
        """Can somebody update a planet he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_planet_create(self):
        """Can somebody create a planet for an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_planet_delete(self):
        """Can somebody delete a planet for an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_account_delete(self):
        """Can somebody delete an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_moon_create(self):
        """Can somebody create a moon in an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_moon_settings_commit(self):
        """Can somebody update a moon in an account he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_moon_delete(self):
        """Can somebody delete a moon in an account he doesn't posess?"""
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

    def test_item_update_no_post(self):
        """What does ``item_update()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_item_update_redirect(self):
        """Does ``item_update()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to referer)
        self.assertEqual(True, True)

    def test_item_update_research_update(self):
        """Does ``item_update()`` correctly update researches?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_ship_update(self):
        """Does ``item_update()`` correctly update ships?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_building_update(self):
        """Does ``item_update()`` correctly update buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_moon_building_update(self):
        """Does ``item_update()`` correctly update moon buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_defense_update(self):
        """Does ``item_update()`` correctly update defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_moon_defense_update(self):
        """Does ``item_update()`` correctly update moon defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(True, True)

    def test_item_update_unknown_item_type(self):
        """Does ``item_update()`` correctly handle unknown item_types?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_create_account_redirect(self):
        """Does ``create_account()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_settings of new account)
        self.assertEqual(True, True)

    def test_account_settings_commit_no_post(self):
        """What does ``account_settings_commit()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_account_settings_commit_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_account_settings_commit_redirect(self):
        """Does ``account_settings_commit()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_settings)
        self.assertEqual(True, True)

    def test_planet_settings_commit_no_post(self):
        """What does ``planet_settings_commit()`` do, if no POST data is provided?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(True, True)

    def test_planet_settings_commit_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_planet_settings_commit_redirect(self):
        """Does ``planet_settings_commit()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings)
        self.assertEqual(True, True)

    def test_planet_create_redirect(self):
        """Does ``planet_create()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to planet_settings of new planet)
        self.assertEqual(True, True)

    def test_planet_delete_get(self):
        """Does a GET to ``planet_delete()`` show the confirmation template?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_planet_delete_redirect(self):
        """Does ``planet_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to account_overview)
        self.assertEqual(True, True)

    def test_planet_delete_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_account_delete_get(self):
        """Does a GET to ``account_delete()`` show the confirmation template?"""
        # TODO insert real test here
        self.assertEqual(True, True)

    def test_account_delete_redirect(self):
        """Does ``planet_delete()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to home)
        self.assertEqual(True, True)

    def test_account_delete_post_tamper(self):
        """What does happen, if somebody tampers POST data?"""
        # TODO insert real test here
        self.assertEqual(True, True)

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

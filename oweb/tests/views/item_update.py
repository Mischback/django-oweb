"""Contains tests for oweb.views.updates.item_update"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
# app imports
from oweb.tests import OWebViewTests


class OWebViewsItemUpdateTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:item_update'))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    @skip('not yet implemented')
    def test_account_owner(self):
        """Can somebody update an item he doesn't posess?"""
        # TODO insert real test here (should raise OWebAccountAccessViolation)
        self.assertEqual(True, True)

    def test_no_post(self):
        """What if no POST data is supplied?"""
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'))
        self.assertEqual(r.status_code, 500)
        self.assertTemplateUsed(r, 'oweb/500.html')

    @skip('not yet implemented')
    def test_redirect(self):
        """Does ``item_update()`` redirect to the correct page?"""
        # TODO insert real test here (should redirect to referer)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_research_update(self):
        """Does ``item_update()`` correctly update researches?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_ship_update(self):
        """Does ``item_update()`` correctly update ships?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_building_update(self):
        """Does ``item_update()`` correctly update buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_moon_building_update(self):
        """Does ``item_update()`` correctly update moon buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_defense_update(self):
        """Does ``item_update()`` correctly update defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_moon_defense_update(self):
        """Does ``item_update()`` correctly update moon defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        # TODO insert real test here (is item updated after finishing?)
        self.assertEqual(False, True)

    @skip('not yet implemented')
    def test_unknown_item_type(self):
        """Does ``item_update()`` correctly handle unknown item_types?"""
        # TODO insert real test here (should raise OWebDoesNotExist)
        self.assertEqual(False, True)

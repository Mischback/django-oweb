"""Contains tests for oweb.views.updates.item_update"""
# Python imports
from unittest import skip
# Django imports
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import User
# app imports
from oweb.tests import OWebViewTests
from oweb.models.account import Account
from oweb.models.research import Research
from oweb.models.ship import Ship
from oweb.models.planet import Planet, Moon
from oweb.models.building import Building
from oweb.models.defense import Defense


@override_settings(AUTH_USER_MODEL='auth.User')
class OWebViewsItemUpdateTests(OWebViewTests):

    def test_login_required(self):
        """Unauthenticated users should be redirected to oweb:app_login"""
        r = self.client.get(reverse('oweb:item_update'))
        self.assertRedirects(r,
                             reverse('oweb:app_login'),
                             status_code=302,
                             target_status_code=200)

    def test_account_owner(self):
        """Can somebody update an item he doesn't posess?"""
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        res_pre = Research.objects.filter(account=acc).first()
        self.client.login(username='test02', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'research',
                                    'item_id': res_pre.id,
                                    'item_level': res_pre.level + 1 },
                             HTTP_REFERER=reverse('oweb:account_research',
                                                  args=[acc.id]))
        self.assertEqual(r.status_code, 403)
        self.assertTemplateUsed(r, 'oweb/403.html')

    def test_no_post(self):
        """What if no POST data is supplied?"""
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'))
        self.assertEqual(r.status_code, 500)
        self.assertTemplateUsed(r, 'oweb/500.html')

    def test_research_update(self):
        """Does ``item_update()`` correctly update researches?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        res_pre = Research.objects.filter(account=acc).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'research',
                                    'item_id': res_pre.id,
                                    'item_level': res_pre.level + 1 },
                             HTTP_REFERER=reverse('oweb:account_research',
                                                  args=[acc.id]))
        self.assertRedirects(r,
                             reverse('oweb:account_research', args=[acc.id]),
                             status_code=302,
                             target_status_code=200)
        res_post = Research.objects.get(pk=res_pre.pk)
        self.assertEqual(res_pre.level + 1, res_post.level)

    def test_ship_update(self):
        """Does ``item_update()`` correctly update ships?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        ship_pre = Ship.objects.filter(account=acc).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'ship',
                                    'item_id': ship_pre.id,
                                    'item_level': ship_pre.count + 1338 },
                             HTTP_REFERER=reverse('oweb:account_ships',
                                                  args=[acc.id]))
        self.assertRedirects(r,
                             reverse('oweb:account_ships', args=[acc.id]),
                             status_code=302,
                             target_status_code=200)
        ship_post = Ship.objects.get(pk=ship_pre.pk)
        self.assertEqual(ship_pre.count + 1338, ship_post.count)

    def test_building_update(self):
        """Does ``item_update()`` correctly update buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        p = Planet.objects.filter(account=acc).first()
        b_pre = Building.objects.filter(astro_object=p).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'building',
                                    'item_id': b_pre.id,
                                    'item_level': b_pre.level - 1 },
                             HTTP_REFERER=reverse('oweb:planet_buildings',
                                                  args=[p.id]))
        self.assertRedirects(r,
                             reverse('oweb:planet_buildings', args=[p.id]),
                             status_code=302,
                             target_status_code=200)
        b_post = Building.objects.get(pk=b_pre.pk)
        self.assertEqual(b_pre.level - 1, b_post.level)

    def test_moon_building_update(self):
        """Does ``item_update()`` correctly update moon buildings?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        p = Planet.objects.filter(account=acc).values_list('id', flat=True)
        m = Moon.objects.filter(planet__in=p).first()
        b_pre = Building.objects.filter(astro_object=m).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'moon_building',
                                    'item_id': b_pre.id,
                                    'item_level': b_pre.level + 2 },
                             HTTP_REFERER=reverse('oweb:moon_buildings',
                                                  args=[m.id]))
        self.assertRedirects(r,
                             reverse('oweb:moon_buildings', args=[m.id]),
                             status_code=302,
                             target_status_code=200)
        b_post = Building.objects.get(pk=b_pre.pk)
        self.assertEqual(b_pre.level + 2, b_post.level)

    def test_defense_update(self):
        """Does ``item_update()`` correctly update defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        p = Planet.objects.filter(account=acc).first()
        d_pre = Defense.objects.filter(astro_object=p).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'defense',
                                    'item_id': d_pre.id,
                                    'item_level': d_pre.count - 1 },
                             HTTP_REFERER=reverse('oweb:planet_defense',
                                                  args=[p.id]))
        self.assertRedirects(r,
                             reverse('oweb:planet_defense', args=[p.id]),
                             status_code=302,
                             target_status_code=200)
        d_post = Defense.objects.get(pk=d_pre.pk)
        self.assertEqual(d_pre.count - 1, d_post.count)

    def test_moon_defense_update(self):
        """Does ``item_update()`` correctly update moon defense devices?
        
        Basically the Django ORM can be trusted, but since there is some logic
        involved in determine the correct field to update, this test is
        included
        """
        u = User.objects.get(username='test01')
        acc = Account.objects.get(owner=u)
        p = Planet.objects.filter(account=acc).values_list('id', flat=True)
        m = Moon.objects.filter(planet__in=p).first()
        d_pre = Defense.objects.filter(astro_object=m).first()
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={ 'item_type': 'moon_defense',
                                    'item_id': d_pre.id,
                                    'item_level': d_pre.count - 10000 },
                             HTTP_REFERER=reverse('oweb:moon_defense',
                                                  args=[m.id]))
        self.assertRedirects(r,
                             reverse('oweb:moon_defense', args=[m.id]),
                             status_code=302,
                             target_status_code=200)
        d_post = Defense.objects.get(pk=d_pre.pk)
        self.assertEqual(0, d_post.count)

    def test_unknown_item_type(self):
        """Does ``item_update()`` correctly handle unknown item_types?"""
        self.client.login(username='test01', password='foo')
        r = self.client.post(reverse('oweb:item_update'),
                             data={
                                 'item_type': 'foobar',
                                 'item_id': 1,
                                 'item_level': 1
                             })
        self.assertEqual(r.status_code, 500)
        self.assertTemplateUsed(r, 'oweb/500.html')

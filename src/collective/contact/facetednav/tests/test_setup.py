# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from collective.contact.facetednav.testing import IntegrationTestCase
from plone import api
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import TEST_USER_NAME
from eea.facetednavigation.interfaces import IPossibleFacetedNavigable

class TestInstall(IntegrationTestCase):
    """Test installation of collective.contact.facetednav into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.contact.facetednav is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.contact.facetednav'))
        self.assertTrue('mydirectory' in self.portal)
        self.assertTrue(IPossibleFacetedNavigable.providedBy(self.portal.mydirectory))

    def test_uninstall(self):
        """Test if collective.contact.facetednav is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.contact.facetednav'])
        self.assertFalse(self.installer.isProductInstalled('collective.contact.facetednav'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveContactFacetednavLayer is registered."""
        from collective.contact.facetednav.interfaces import ICollectiveContactFacetednavLayer
        from plone.browserlayer import utils
        self.failUnless(ICollectiveContactFacetednavLayer in utils.registered_layers())

    def test_subtyper(self):
        login(self.portal, TEST_USER_NAME)
        directory = self.portal.mydirectory
        subtyper = directory.unrestrictedTraverse('@@contact_faceted_subtyper')

        subtyper.enable_select()
        self.assertTrue(subtyper.can_select)
        self.assertFalse(subtyper.can_enable_select())
        self.assertTrue(subtyper.can_disable_select())
        self.assertTrue(directory.unrestrictedTraverse('@@faceted_query').is_selectable())

        subtyper.disable_select()
        self.assertFalse(subtyper.can_select)
        self.assertTrue(subtyper.can_enable_select())
        self.assertFalse(subtyper.can_disable_select())
        self.assertFalse(directory.unrestrictedTraverse('@@faceted_query').is_selectable())

    def test_json_contacts(self):
        login(self.portal, TEST_USER_NAME)
        directory = self.portal.mydirectory

        self.portal.REQUEST.form['type'] = 'organization'
        json_contacts = eval(directory.unrestrictedTraverse('@@json-contacts')())
        self.assertEqual(len(json_contacts), 7)
        self.assertTrue(json_contacts[0].has_key('id'))
        self.assertEqual(json_contacts[0]['path'], '/plone/mydirectory/armeedeterre')

        self.portal.REQUEST.form['type'] = 'held_position'
        json_contacts = eval(directory.unrestrictedTraverse('@@json-contacts')())
        self.assertEqual(len(json_contacts), 4)
        self.assertEqual(json_contacts[0]['path'], '/plone/mydirectory/degaulle/adt')

    def test_delete_action(self):
        login(self.portal, TEST_USER_NAME)
        directory = self.portal.mydirectory

        self.assertIn('rambo', directory)
        self.portal.REQUEST.form['uids'] = [directory.rambo.UID()]
        delete_view = directory.unrestrictedTraverse('@@delete_selection')
        delete_view()
        self.assertNotIn('rambo', directory)
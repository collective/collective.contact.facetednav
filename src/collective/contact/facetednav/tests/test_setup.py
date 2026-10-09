# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""
from collective.contact.facetednav.interfaces import ICollectiveContactFacetednavLayer
from collective.contact.facetednav.testing import IntegrationTestCase
from eea.facetednavigation.interfaces import IPossibleFacetedNavigable
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import TEST_USER_NAME
from plone.base.utils import get_installer
from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface.declarations import alsoProvides

import json


BUNDLE = "plone.bundles/collective-contact-facetednav"


class TestInstall(IntegrationTestCase):
    """Test installation of collective.contact.facetednav into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if collective.contact.facetednav is installed."""
        self.assertTrue(self.installer.is_product_installed("collective.contact.facetednav"))
        self.assertTrue("mydirectory" in self.portal)
        self.assertTrue(IPossibleFacetedNavigable.providedBy(self.portal.mydirectory))

    def test_uninstall(self):
        """Test if collective.contact.facetednav is cleanly uninstalled."""
        self.installer.uninstall_product("collective.contact.facetednav")
        self.assertFalse(self.installer.is_product_installed("collective.contact.facetednav"))

    def test_uninstall_plone6(self):
        """The uninstall profile removes the browser layer, the bundle and the actions."""
        self.installer.uninstall_product("collective.contact.facetednav")
        self.assertNotIn(ICollectiveContactFacetednavLayer, utils.registered_layers())
        self.assertNotIn(BUNDLE + ".jscompilation", getUtility(IRegistry))
        self.assertNotIn("faceted.actions.enable", self.portal.portal_actions.object_buttons)
        self.assertNotIn("faceted.actions.disable", self.portal.portal_actions.object_buttons)

    # registry.xml
    def test_bundle_plone6(self):
        """A classic script deferred after eea.facetednavigation's faceted.view bundle."""
        registry = getUtility(IRegistry)
        self.assertEqual(registry[BUNDLE + ".jscompilation"], "++resource++collective.contact.facetednav/javascript.js")
        self.assertEqual(registry[BUNDLE + ".csscompilation"], "++resource++collective.contact.facetednav/style.css")
        self.assertEqual(registry[BUNDLE + ".depends"], "faceted.view")
        self.assertTrue(registry[BUNDLE + ".load_defer"])
        self.assertFalse(registry[BUNDLE + ".load_async"])
        self.assertIn("faceted.actions.enable", self.portal.portal_actions.object_buttons)

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that ICollectiveContactFacetednavLayer is registered."""
        self.assertTrue(ICollectiveContactFacetednavLayer in utils.registered_layers())

    def test_subtyper(self):
        login(self.portal, TEST_USER_NAME)
        directory = self.portal.mydirectory
        alsoProvides(self.portal.REQUEST, ICollectiveContactFacetednavLayer)
        subtyper = directory.unrestrictedTraverse("@@contact_faceted_subtyper")
        subtyper.enable_actions()
        self.assertTrue(subtyper.actions_enabled)
        self.assertFalse(subtyper.can_enable_actions())
        self.assertTrue(subtyper.can_disable_actions())
        self.assertTrue(directory.unrestrictedTraverse("@@faceted_query").actions_enabled())

        subtyper.disable_actions()
        self.assertFalse(subtyper.actions_enabled)
        self.assertTrue(subtyper.can_enable_actions())
        self.assertFalse(subtyper.can_disable_actions())
        self.assertFalse(directory.unrestrictedTraverse("@@faceted_query").actions_enabled())

    def test_json_contacts(self):
        login(self.portal, TEST_USER_NAME)
        alsoProvides(self.portal.REQUEST, ICollectiveContactFacetednavLayer)
        directory = self.portal.mydirectory

        self.portal.REQUEST.form["type"] = "organization"
        json_contacts = json.loads(directory.unrestrictedTraverse("@@json-contacts")())
        self.assertEqual(len(json_contacts), 7)
        self.assertTrue("id" in json_contacts[0])
        self.assertEqual(json_contacts[0]["path"], "/plone/mydirectory/armeedeterre")

        self.portal.REQUEST.form["type"] = "held_position"
        json_contacts = json.loads(directory.unrestrictedTraverse("@@json-contacts")())
        self.assertEqual(len(json_contacts), 6)
        self.assertEqual(json_contacts[0]["path"], "/plone/mydirectory/degaulle/adt")

    def test_json_contacts_select_all_max(self):
        login(self.portal, TEST_USER_NAME)
        alsoProvides(self.portal.REQUEST, ICollectiveContactFacetednavLayer)
        directory = self.portal.mydirectory

        self.portal.REQUEST.form["type"] = "organization"
        self.portal.REQUEST.form["cfn_select_all_max"] = 5
        json_contacts = json.loads(directory.unrestrictedTraverse("@@json-contacts")())
        self.assertEqual(len(json_contacts), 6)

    def test_delete_action(self):
        login(self.portal, TEST_USER_NAME)
        directory = self.portal.mydirectory

        self.assertIn("rambo", directory)
        self.portal.REQUEST.form["uids"] = [directory.rambo.UID()]
        delete_view = directory.unrestrictedTraverse("@@delete_selection")
        delete_view()
        self.assertNotIn("rambo", directory)

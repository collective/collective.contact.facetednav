# -*- coding: utf-8 -*-
"""Install profile (profiles/default) and uninstall."""

from collective.contact.facetednav.interfaces import ICollectiveContactFacetednavLayer
from collective.contact.facetednav.testing import IntegrationTestCase
from eea.facetednavigation.interfaces import IPossibleFacetedNavigable
from plone import api
from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:  # Plone < 5.1
    get_installer = None


PACKAGE = "collective.contact.facetednav"
JS = "++resource++collective.contact.facetednav/javascript.js"
CSS = "++resource++collective.contact.facetednav/style.css"
BEHAVIOR = "eea.faceted.navigable"
ACTIONS = ("faceted.actions.enable", "faceted.actions.disable")


def is_installed(portal, product):
    if get_installer is None:
        return api.portal.get_tool("portal_quickinstaller").isProductInstalled(product)
    return get_installer(portal).is_product_installed(product)


def uninstall(portal, product):
    if get_installer is None:
        api.portal.get_tool("portal_quickinstaller").uninstallProducts([product])
    else:
        get_installer(portal).uninstall_product(product)


def registered_resources(portal):
    """ids of the css and js resources: portal_css/portal_javascripts (Plone 4) or registry bundles"""
    if "portal_css" in portal.objectIds():
        return set(api.portal.get_tool("portal_css").getResourceIds()) | set(
            api.portal.get_tool("portal_javascripts").getResourceIds()
        )
    registry = getUtility(IRegistry)
    return set(
        registry[name]
        for name in registry.records.keys()
        if name.startswith("plone.bundles/") and name.endswith("compilation")
    )


def object_buttons(portal):
    return api.portal.get_tool("portal_actions").object_buttons


class TestInstall(IntegrationTestCase):
    """Test installation of collective.contact.facetednav into Plone."""

    def test_product_installed(self):
        self.assertTrue(is_installed(self.portal, PACKAGE))
        # metadata.xml dependencies (collective.js.backbone dropped on Plone 6)
        setup = api.portal.get_tool("portal_setup")
        for profile in ("collective.contact.core:default", "eea.facetednavigation:default"):
            self.assertNotEqual(setup.getLastVersionForProfile(profile), "unknown", profile)

    # browserlayer.xml
    def test_browserlayer(self):
        self.assertIn(ICollectiveContactFacetednavLayer, utils.registered_layers())

    # actions.xml
    def test_actions(self):
        buttons = object_buttons(self.portal)
        for action_id in ACTIONS:
            action = buttons[action_id]
            name = action_id.split(".")[-1]
            self.assertEqual(
                action.url_expr, "string:${object/absolute_url}/@@contact_faceted_subtyper/%s_actions" % name
            )
            self.assertEqual(action.available_expr, "object/@@contact_faceted_subtyper/can_%s_actions" % name)
            self.assertEqual(action.permissions, ("eea.facetednavigation: Configure faceted",))
            self.assertTrue(action.visible)

    # types/directory.xml
    def test_directory_behavior(self):
        fti = api.portal.get_tool("portal_types").directory
        self.assertIn(BEHAVIOR, fti.behaviors)
        self.assertTrue(IPossibleFacetedNavigable.providedBy(self.directory))

    # cssregistry.xml, jsregistry.xml
    def test_resources(self):
        resources = registered_resources(self.portal)
        self.assertIn(JS, resources)
        self.assertIn(CSS, resources)

    # registry.xml
    def test_bundle(self):
        """classic script deferred after eea.facetednavigation's faceted.view bundle"""
        registry = getUtility(IRegistry)
        bundle = "plone.bundles/collective-contact-facetednav"
        self.assertEqual(registry[bundle + ".jscompilation"], JS)
        self.assertEqual(registry[bundle + ".csscompilation"], CSS)
        self.assertEqual(registry[bundle + ".depends"], "faceted.view")
        self.assertTrue(registry[bundle + ".load_defer"])
        self.assertFalse(registry[bundle + ".load_async"])

    def test_uninstall(self):
        uninstall(self.portal, PACKAGE)
        self.assertFalse(is_installed(self.portal, PACKAGE))
        self.assertNotIn(ICollectiveContactFacetednavLayer, utils.registered_layers())
        buttons = object_buttons(self.portal)
        for action_id in ACTIONS:
            self.assertNotIn(action_id, buttons.objectIds())
        resources = registered_resources(self.portal)
        self.assertNotIn(JS, resources)
        self.assertNotIn(CSS, resources)

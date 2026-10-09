# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from collective.contact.facetednav.interfaces import ICollectiveContactFacetednavLayer
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.component import getMultiAdapter
from zope.globalrequest import clearRequest
from zope.globalrequest import setLocal
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import collective.contact.core
import collective.contact.facetednav
import os
import transaction
import unittest


try:
    from plone.testing.zope import installProduct
    from plone.testing.zope import uninstallProduct
    from plone.testing.zope import WSGI_SERVER_FIXTURE as SERVER_FIXTURE
except ImportError:  # Plone 4
    from plone.testing.z2 import installProduct
    from plone.testing.z2 import uninstallProduct
    from plone.testing.z2 import ZSERVER_FIXTURE as SERVER_FIXTURE

try:  # profile dependency on Plone 4 only (no Backbone on Plone 6)
    import collective.js.backbone as backbone
except ImportError:
    backbone = None


FACETED_XML = os.path.join(os.path.dirname(__file__), "tests", "contacts-faceted.xml")


class CollectiveContactFacetednavLayer(PloneSandboxLayer):
    """collective.contact.core test data; mydirectory is a faceted navigation
    (tests/contacts-faceted.xml), contact actions disabled (as after install)."""

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        self.loadZCML(package=collective.contact.facetednav, name="testing.zcml")
        if backbone is not None:
            self.loadZCML(package=backbone)
        installProduct(app, "collective.contact.facetednav")
        self.loadZCML(package=collective.contact.core, name="testing.zcml")

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        setLocal("request", portal.REQUEST)  # collective.fingerpointing (imio.fpaudit) needs a request
        applyProfile(portal, "collective.contact.core:testing")
        applyProfile(portal, "collective.contact.core:test_data")
        applyProfile(portal, "collective.contact.facetednav:testing")
        try:  # javascript of the collective.contact.widget widgets (@@add-contact), installed on a Plone 4 site
            applyProfile(portal, "plone.formwidget.contenttree:default")
        except KeyError:  # not registered (testing.zcml)
            pass
        directory = portal.mydirectory
        directory.unrestrictedTraverse("@@faceted_subtyper").enable()
        with open(FACETED_XML, "rb") as import_file:
            directory.unrestrictedTraverse("@@faceted_exportimport")._import_xml(import_file=import_file)
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        transaction.commit()
        clearRequest()  # else the next layers get a request bound to a closed connection (Plone 6.2)

    def tearDownZope(self, app):
        """Tear down Zope."""
        uninstallProduct(app, "collective.contact.facetednav")


FIXTURE = CollectiveContactFacetednavLayer(name="FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="INTEGRATION")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="FUNCTIONAL")

ACCEPTANCE = FunctionalTesting(bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, SERVER_FIXTURE), name="ACCEPTANCE")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests: Manager, request on the package browser layer."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.directory = self.portal.mydirectory
        alsoProvides(self.request, ICollectiveContactFacetednavLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        login(self.portal, TEST_USER_NAME)

    def viewlet_manager(self, name, context, view_name):
        """updated viewlet manager, as rendered by the view_name view of context"""
        view = context.restrictedTraverse(view_name)
        manager = getMultiAdapter((context, self.request, view), IViewletManager, name=name)
        manager.update()
        return manager


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

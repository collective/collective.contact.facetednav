# -*- coding: utf-8 -*-
"""Base module for unittesting."""
import os

import collective.contact.core
import collective.contact.facetednav

import pkg_resources
import unittest2 as unittest
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.testing import z2
from zope.interface import alsoProvides
from .setuphandlers import create_test_contact_data, create_test_held_positions

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PA_CONTENTTYPES = False
else:
    HAS_PA_CONTENTTYPES = True


class CollectiveContactFacetednavLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=collective.contact.facetednav,
                      name='testing.zcml')
        z2.installProduct(app, 'collective.contact.facetednav')
        self.loadZCML(package=collective.contact.core,
                      name='testing.zcml')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        super(CollectiveContactFacetednavLayer, self).setUpPloneSite(portal)
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.contact.core:testing')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        create_test_contact_data(portal)
        if create_test_held_positions:
            create_test_held_positions(portal)
        applyProfile(portal, 'collective.contact.facetednav:default')
        alsoProvides(portal.mydirectory, IFacetedNavigable)
        portal.mydirectory.unrestrictedTraverse('@@faceted_exportimport')._import_xml(
            import_file=open(os.path.dirname(__file__) + '/tests/contacts-faceted.xml'))

        # Commit so that the test browser sees these objects
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.contact.facetednav')


FIXTURE = CollectiveContactFacetednavLayer(
    name="FIXTURE"
)

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,),
    name="INTEGRATION"
)

FUNCTIONAL = FunctionalTesting(
    bases=(FIXTURE,),
    name="FUNCTIONAL"
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer['portal']


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

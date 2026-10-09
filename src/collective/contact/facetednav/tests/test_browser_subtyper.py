# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from collective.contact.facetednav.browser.subtyper import ContactFacetedPublicSubtyper
from collective.contact.facetednav.browser.subtyper import ContactFacetedSubtyper
from collective.contact.facetednav.interfaces import IActionsEnabled
from collective.contact.facetednav.testing import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides
from zope.publisher.interfaces import NotFound


def messages(request):
    """status messages of the request (they accumulate in a test request)"""
    return [message.message for message in IStatusMessage(request).show()]


class TestContactFacetedPublicSubtyper(IntegrationTestCase):
    """@@contact_faceted_subtyper of the contents that can't be faceted (a person)"""

    def setUp(self):
        super(TestContactFacetedPublicSubtyper, self).setUp()
        self.person = self.directory.rambo
        self.subtyper = self.person.restrictedTraverse("@@contact_faceted_subtyper")

    def test_actions_enabled(self):
        self.assertIsInstance(self.subtyper, ContactFacetedPublicSubtyper)
        self.assertNotIsInstance(self.subtyper, ContactFacetedSubtyper)
        self.assertFalse(self.subtyper.actions_enabled)
        alsoProvides(self.person, IActionsEnabled)
        self.assertTrue(self.subtyper.actions_enabled)

    def test_can_enable_actions(self):
        self.assertFalse(self.subtyper.can_enable_actions())

    def test_can_disable_actions(self):
        alsoProvides(self.person, IActionsEnabled)
        self.assertFalse(self.subtyper.can_disable_actions())

    def test_enable_actions(self):
        self.assertRaises(NotFound, self.subtyper.enable_actions)
        self.assertFalse(IActionsEnabled.providedBy(self.person))

    def test_disable_actions(self):
        self.assertRaises(NotFound, self.subtyper.disable_actions)

    def test__redirect(self):
        self.assertEqual(self.subtyper._redirect(), "")
        self.assertEqual(self.request.response.getHeader("location"), "http://nohost/plone/mydirectory/rambo")
        self.assertEqual(messages(self.request), [])
        self.assertEqual(self.subtyper._redirect("Done"), "Done")
        self.assertEqual(messages(self.request), ["Done"])


class TestContactFacetedSubtyper(IntegrationTestCase):
    """@@contact_faceted_subtyper of a faceted directory (Actions menu: actions.xml)"""

    def setUp(self):
        super(TestContactFacetedSubtyper, self).setUp()
        self.subtyper = self.directory.restrictedTraverse("@@contact_faceted_subtyper")

    def test_can_enable_actions(self):
        self.assertIsInstance(self.subtyper, ContactFacetedSubtyper)
        self.assertTrue(self.subtyper.can_enable_actions())
        alsoProvides(self.directory, IActionsEnabled)
        self.assertFalse(self.subtyper.can_enable_actions())

    def test_can_disable_actions(self):
        self.assertFalse(self.subtyper.can_disable_actions())
        alsoProvides(self.directory, IActionsEnabled)
        self.assertTrue(self.subtyper.can_disable_actions())

    def test_enable_actions(self):
        self.subtyper.enable_actions()
        self.assertTrue(IActionsEnabled.providedBy(self.directory))
        self.assertTrue(self.subtyper.actions_enabled)
        self.assertEqual(self.request.response.getHeader("location"), "http://nohost/plone/mydirectory")
        self.assertEqual(messages(self.request), ["Contacts actions enabled"])
        # already enabled
        self.subtyper.enable_actions()
        self.assertTrue(IActionsEnabled.providedBy(self.directory))
        self.assertEqual(messages(self.request)[-1], "Faceted navigation not supported")
        # needs the "eea.facetednavigation: Configure faceted" permission
        setRoles(self.portal, TEST_USER_ID, ["Member", "Reader"])
        self.assertRaises(Unauthorized, self.directory.restrictedTraverse, "@@contact_faceted_subtyper")

    def test_disable_actions(self):
        alsoProvides(self.directory, IActionsEnabled)
        self.subtyper.disable_actions()
        self.assertFalse(IActionsEnabled.providedBy(self.directory))
        self.assertFalse(self.subtyper.actions_enabled)
        self.assertEqual(self.request.response.getHeader("location"), "http://nohost/plone/mydirectory")
        self.assertEqual(messages(self.request), ["Contacts actions disabled"])
        # already disabled
        self.subtyper.disable_actions()
        self.assertFalse(IActionsEnabled.providedBy(self.directory))
        self.assertEqual(messages(self.request)[-1], "Contacts actions disabled")

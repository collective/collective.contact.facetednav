# -*- coding: utf-8 -*-
from collective.contact.facetednav.browser.actions.manager import ActionsViewletManager
from collective.contact.facetednav.browser.actions.manager import BatchActionsViewletManager
from collective.contact.facetednav.browser.actions.manager import is_available
from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY
from collective.contact.facetednav.testing import IntegrationTestCase
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.statusmessages.interfaces import IStatusMessage

import unittest


BATCH_ACTIONS = "collective.contact.facetednav.batchactions"
ACTIONS = "collective.contact.facetednav.actions"


class TestManager(IntegrationTestCase):
    """module functions"""

    def test_is_available(self):
        manager = self.viewlet_manager(BATCH_ACTIONS, self.directory, "@@faceted_query")
        viewlet, excel = manager.viewlets
        self.assertTrue(is_available(viewlet))
        viewlet.available = False
        self.assertFalse(is_available(viewlet))
        viewlet.available = lambda: False
        self.assertFalse(is_available(viewlet))
        del viewlet.available
        # the viewlet permission (zope2.DeleteObjects) protects render
        setRoles(self.portal, TEST_USER_ID, ["Member", "Reader"])
        self.assertFalse(is_available(viewlet))
        self.assertTrue(is_available(excel))


class TestConditionalViewletManager(IntegrationTestCase):

    def test_filter(self):
        manager = self.viewlet_manager(BATCH_ACTIONS, self.directory, "@@faceted_query")
        delete, excel = manager.viewlets
        self.assertEqual(manager.filter([("delete", delete), ("excel", excel)]), [("delete", delete), ("excel", excel)])
        delete.available = False
        self.assertEqual(manager.filter([("delete", delete), ("excel", excel)]), [("excel", excel)])


class TestBatchActionsViewletManager(IntegrationTestCase):
    """batch actions above the faceted results (batchactions.pt)"""

    def test_render(self):
        manager = self.viewlet_manager(BATCH_ACTIONS, self.directory, "@@faceted_query")
        self.assertIsInstance(manager, BatchActionsViewletManager)
        # weight order: delete (500), excel export (800)
        self.assertEqual([viewlet.name for viewlet in manager.viewlets], ["delete", "excelexport"])
        html = manager.render()
        self.assertIn('id="contacts-facetednav-batchactions"', html)
        self.assertIn('id="contacts-selectall"', html)
        self.assertIn('data-select-all-msg="Select all"', html)
        self.assertIn('data-unselect-all-msg="Unselect all"', html)
        self.assertIn('data-select-all-too-large-msg="Results is too large for mass selection"', html)
        self.assertLess(
            html.index('id="contact-facetednav-action-delete"'),
            html.index('id="contact-facetednav-action-excelexport"'),
        )
        self.assertIn('id="contacts-selection-num"', html)
        self.assertIn('<span class="num">0</span>', html)
        # status messages (e.g. of @@delete_selection) are shown above the batch actions
        IStatusMessage(self.request).add("2 object(s) deleted")
        self.assertIn("2 object(s) deleted", manager.render())
        # without the delete permission
        setRoles(self.portal, TEST_USER_ID, ["Member", "Reader"])
        manager = self.viewlet_manager(BATCH_ACTIONS, self.directory, "@@faceted_query")
        self.assertEqual([viewlet.name for viewlet in manager.viewlets], ["excelexport"])
        self.assertNotIn("contact-facetednav-action-delete", manager.render())


class TestActionsViewletManager(IntegrationTestCase):
    """actions of each contact of the faceted results"""

    def test_available(self):
        manager = self.viewlet_manager(ACTIONS, self.directory.rambo, "@@faceted-preview-item")
        self.assertIsInstance(manager, ActionsViewletManager)
        self.request.set(ACTIONS_ENABLED_KEY, False)
        self.assertFalse(manager.available())
        self.request.set(ACTIONS_ENABLED_KEY, True)
        self.assertTrue(manager.available())

    @unittest.expectedFailure
    def test_available_outside_faceted_query(self):
        """Plone 4 bug: KeyError when the key isn't set by @@faceted_query (preview item rendered elsewhere)"""
        manager = self.viewlet_manager(ACTIONS, self.directory.rambo, "@@faceted-preview-item")
        self.assertFalse(manager.available())

    def test_render(self):
        self.request.set(ACTIONS_ENABLED_KEY, True)
        manager = self.viewlet_manager(ACTIONS, self.directory.rambo, "@@faceted-preview-item")
        # weight order: edit (200), delete (1000)
        self.assertEqual([viewlet.name for viewlet in manager.viewlets], ["edit-contact", "delete-contact"])
        html = manager.render()
        self.assertIn('class="contacts-facetednav-actions"', html)
        self.assertEqual(html.count('class="contacts-facetednav-action"'), 2)
        self.request.set(ACTIONS_ENABLED_KEY, False)
        self.assertNotIn("contacts-facetednav-actions", manager.render())
        # a Reader has no action
        self.request.set(ACTIONS_ENABLED_KEY, True)
        setRoles(self.portal, TEST_USER_ID, ["Member", "Reader"])
        manager = self.viewlet_manager(ACTIONS, self.directory.rambo, "@@faceted-preview-item")
        self.assertEqual(manager.viewlets, [])
        self.assertNotIn('contacts-facetednav-action"', manager.render())

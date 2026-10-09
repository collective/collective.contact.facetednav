# -*- coding: utf-8 -*-
from collective.contact.facetednav.browser.actions.delete import DeleteAction
from collective.contact.facetednav.browser.actions.delete import DeleteBatchAction
from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY
from collective.contact.facetednav.testing import IntegrationTestCase
from Products.statusmessages.interfaces import IStatusMessage

import json


class TestDeleteBatchAction(IntegrationTestCase):

    def setUp(self):
        super(TestDeleteBatchAction, self).setUp()
        manager = self.viewlet_manager("collective.contact.facetednav.batchactions", self.directory, "@@faceted_query")
        self.viewlet = manager.viewlets[0]

    def test_onclick(self):
        self.assertIsInstance(self.viewlet, DeleteBatchAction)
        # $num is replaced by javascript
        self.assertEqual(
            self.viewlet.onclick,
            "contactfacetednav.delete_selection(" '"Are you sure you want to remove $num selected content(s) ?")',
        )

    def test_render(self):
        html = self.viewlet.render()
        self.assertIn('id="contact-facetednav-action-delete"', html)
        self.assertIn('name="delete"', html)
        self.assertIn('class="destructive"', html)
        self.assertIn('value="Delete selected contacts"', html)
        self.assertIn('onclick="contactfacetednav.delete_selection(', html)


class TestDeleteSelection(IntegrationTestCase):
    """@@delete_selection, posted by contactfacetednav.delete_selection"""

    def delete_selection(self, *contents):
        self.request.form["uids"] = [content.UID() for content in contents]
        self.request.set("uids", self.request.form["uids"])  # request.get reads 'other' first
        return json.loads(self.directory.restrictedTraverse("@@delete_selection")())

    def test_delete(self):
        self.assertEqual(self.delete_selection(self.directory.rambo, self.directory.draper), {"status": "success"})
        self.assertNotIn("rambo", self.directory)
        self.assertNotIn("draper", self.directory)
        self.assertEqual(self.request.response.getHeader("Content-Type"), "text/json; charset=utf-8")
        self.assertEqual(self.request.response.getHeader("Cache-Control"), "no-cache")
        self.assertEqual(
            [(m.message, m.type) for m in IStatusMessage(self.request).show()], [("2 object(s) deleted", "info")]
        )
        # a content the user may not delete (e.g. its workflow state) is kept
        pepper = self.directory.pepper
        pepper.manage_permission("Delete objects", roles=[], acquire=False)
        self.assertEqual(self.delete_selection(pepper, self.directory.degaulle), {"status": "success"})
        self.assertIn("pepper", self.directory)
        self.assertNotIn("degaulle", self.directory)
        self.assertEqual(
            [(m.message, m.type) for m in IStatusMessage(self.request).show()],
            [
                ("1 object(s) deleted", "info"),
                ("1 object(s) were not deleted : Unauthorized: /plone/mydirectory/pepper", "error"),
            ],
        )


class TestDeleteAction(IntegrationTestCase):

    def setUp(self):
        super(TestDeleteAction, self).setUp()
        self.request.set(ACTIONS_ENABLED_KEY, True)
        manager = self.viewlet_manager(
            "collective.contact.facetednav.actions", self.directory.rambo, "@@faceted-preview-item"
        )
        self.viewlet = manager.viewlets[1]

    def test_url(self):
        self.assertIsInstance(self.viewlet, DeleteAction)
        self.assertEqual(self.viewlet.url(), "http://nohost/plone/mydirectory/rambo/delete_confirmation")

    def test_render(self):
        html = self.viewlet.render()
        self.assertIn('href="http://nohost/plone/mydirectory/rambo/delete_confirmation"', html)
        self.assertIn('class="delete-contact"', html)
        self.assertIn('id="contact-action-delete-contact-%s"' % self.directory.rambo.UID(), html)
        self.assertIn('src="http://nohost/plone/++plone++bootstrap-icons/trash.svg"', html)  # @@iconresolver
        self.assertIn('title="Delete this contact"', html)

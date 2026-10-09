# -*- coding: utf-8 -*-
from collective.contact.facetednav.browser.actions.edit import EditAction
from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY
from collective.contact.facetednav.testing import IntegrationTestCase


class TestEditAction(IntegrationTestCase):

    def setUp(self):
        super(TestEditAction, self).setUp()
        self.request.set(ACTIONS_ENABLED_KEY, True)
        manager = self.viewlet_manager(
            "collective.contact.facetednav.actions", self.directory.armeedeterre, "@@faceted-preview-item"
        )
        self.viewlet = manager.viewlets[0]

    def test_url(self):
        self.assertIsInstance(self.viewlet, EditAction)
        self.assertEqual(self.viewlet.url(), "http://nohost/plone/mydirectory/armeedeterre/edit")

    def test_render(self):
        html = self.viewlet.render()
        self.assertIn('href="http://nohost/plone/mydirectory/armeedeterre/edit"', html)
        self.assertIn('class="edit-contact"', html)
        self.assertIn('id="contact-action-edit-contact-%s"' % self.directory.armeedeterre.UID(), html)
        self.assertIn('src="http://nohost/plone/++plone++bootstrap-icons/pencil-square.svg"', html)  # @@iconresolver
        self.assertIn('title="Edit"', html)

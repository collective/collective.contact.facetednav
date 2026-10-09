# -*- coding: utf-8 -*-
"""Rendering of the faceted directory on Plone 6.2 (migration, phase 7)."""

from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY
from collective.contact.facetednav.interfaces import IActionsEnabled
from collective.contact.facetednav.interfaces import ICollectiveContactFacetednavLayer
from collective.contact.facetednav.testing import IntegrationTestCase
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from zope.interface import alsoProvides


CORE_STATIC = "http://nohost/plone/++resource++collective.contact.core/"


class Plone6TestCase(IntegrationTestCase):

    def setUp(self):
        super(Plone6TestCase, self).setUp()
        self.request = self.layer["request"]
        alsoProvides(self.request, ICollectiveContactFacetednavLayer)
        login(self.portal, TEST_USER_NAME)
        self.directory = self.portal.mydirectory


class TestContactsFacetedQueryHandler(Plone6TestCase):

    def test___call___plone6(self):
        """@@faceted_query renders the results (was a KeyError on global_defines)"""
        uid = self.directory.degaulle.UID()
        self.request.form["type[]"] = "person"
        html = self.directory.restrictedTraverse("@@faceted_query")()
        self.assertIn('<span class="contact-title">Général Charles De Gaulle</span>', html)
        self.assertIn('<span class="contact-title">Mister Pepper</span>', html)
        self.assertIn('class="faceted-add-person"', html)
        self.assertIn('<img src="%screate_contact.png" />' % CORE_STATIC, html)
        # actions disabled: no selection, no actions
        self.assertNotIn('id="contact-%s"' % uid, html)
        self.assertNotIn("contacts-facetednav-batchactions", html)
        self.assertNotIn("edit-contact", html)

        alsoProvides(self.directory, IActionsEnabled)
        html = self.directory.restrictedTraverse("@@faceted_query")()
        self.assertIn('<input type="checkbox" value="%s" id="contact-%s" />' % (uid, uid), html)
        self.assertIn('id="contacts-selectall"', html)
        self.assertIn('id="contact-facetednav-action-delete"', html)
        self.assertIn('<span class="num">0</span>', html)
        # per-contact actions, icons from @@iconresolver
        self.assertIn('id="contact-action-edit-contact-%s"' % uid, html)
        self.assertIn('<img src="http://nohost/plone/++plone++bootstrap-icons/pencil-square.svg" alt="Edit"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/degaulle/delete_confirmation"', html)
        self.assertIn('<img src="http://nohost/plone/++plone++bootstrap-icons/trash.svg"', html)
        # the faceted page renders the results too (server side)
        page = self.directory.restrictedTraverse("@@facetednavigation_view")()
        self.assertIn('id="contact-%s"' % uid, page)

        self.request.form["type[]"] = "organization"
        html = self.directory.restrictedTraverse("@@faceted_query")()
        self.assertIn('<span class="organization-title">Armée de terre</span>', html)
        self.assertIn('class="faceted-add-organization"', html)
        self.assertIn('<img src="%sorganization_icon.png" />' % CORE_STATIC, html)


class TestPreviewItem(Plone6TestCase):

    def test___call___plone6(self):
        """preview of the 3 contact types (was a KeyError on portal_properties)"""
        self.request.set(ACTIONS_ENABLED_KEY, False)
        degaulle = self.directory.degaulle
        html = degaulle.restrictedTraverse("@@faceted-preview-item")()
        self.assertIn('<span class="contact-title">Général Charles De Gaulle</span>', html)
        self.assertIn('src="%sdefaultUser.png"' % CORE_STATIC, html)
        self.assertIn('<a href="http://nohost/plone/mydirectory/degaulle/adt">', html)
        self.assertNotIn("contacts-facetednav-actions", html)

        html = degaulle.adt.restrictedTraverse("@@faceted-preview-item")()
        self.assertIn('<span class="contact-title">', html)
        self.assertIn('src="%sdefaultUser.png"' % CORE_STATIC, html)

        html = self.directory.armeedeterre.restrictedTraverse("@@faceted-preview-item")()
        self.assertIn('<span class="organization-title">Armée de terre</span>', html)

        self.request.set(ACTIONS_ENABLED_KEY, True)
        html = degaulle.restrictedTraverse("@@faceted-preview-item")()
        self.assertIn('class="contacts-facetednav-actions"', html)

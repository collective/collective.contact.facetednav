# -*- coding: utf-8 -*-
from collective.contact.facetednav.browser.view import ACTIONS_ENABLED_KEY
from collective.contact.facetednav.browser.view import json_output
from collective.contact.facetednav.interfaces import IActionsEnabled
from collective.contact.facetednav.testing import IntegrationTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides

import json
import unittest


class TestView(IntegrationTestCase):
    """module functions"""

    def test_json_output(self):
        @json_output
        def method(value, key="id"):
            return [{key: value}]

        self.assertEqual(json.loads(method("Général", key="title")), [{"title": "Général"}])
        self.assertEqual(json.loads(method(None)), [{"id": None}])


class TestContactsFacetedQueryHandler(IntegrationTestCase):
    """@@faceted_query: query.pt, preview-items.pt (faceted layout of the directory)"""

    def faceted_query(self, **form):
        self.request.form.update(form)
        for key, value in form.items():  # request.get reads 'other' first: stale after the first query
            self.request.set(key, value)
        return self.directory.restrictedTraverse("@@faceted_query")()

    def test_actions_enabled(self):
        view = self.directory.restrictedTraverse("@@faceted_query")
        self.assertFalse(view.actions_enabled())
        self.assertFalse(self.request[ACTIONS_ENABLED_KEY])
        alsoProvides(self.directory, IActionsEnabled)
        self.assertTrue(view.actions_enabled())
        self.assertTrue(self.request[ACTIONS_ENABLED_KEY])

    def test___call__(self):
        # contacts of the type criterion
        html = self.faceted_query(**{"type[]": "organization"})
        self.assertIn("Armée de terre", html)
        self.assertIn("Corps B", html)
        self.assertNotIn("Rambo", html)
        self.assertEqual(html.count('class="contact-entry"'), 7)
        html = self.faceted_query(**{"type[]": "person"})
        self.assertIn("Rambo", html)
        self.assertNotIn("Corps B", html)
        self.assertEqual(html.count('class="contact-entry"'), 4)
        html = self.faceted_query(**{"type[]": "held_position"})
        self.assertIn("Sergent de la brigade LH", html)
        self.assertEqual(html.count('class="contact-entry"'), 6)
        # actions disabled: no selection, no batch actions, no contact actions
        self.assertNotIn("contact-selection", html)
        self.assertNotIn("contacts-facetednav-batchactions", html)
        self.assertNotIn("contacts-facetednav-actions", html)
        # actions enabled
        alsoProvides(self.directory, IActionsEnabled)
        html = self.faceted_query(**{"type[]": "person"})
        rambo = self.directory.rambo.UID()
        self.assertIn('id="contact-%s"' % rambo, html)
        self.assertEqual(html.count('type="checkbox"'), 4)
        self.assertEqual(html.count('class="contact-selection"'), 4)
        self.assertEqual(html.count('id="contacts-facetednav-batchactions"'), 1)
        self.assertEqual(html.count('class="contacts-facetednav-actions"'), 4)
        # add links of the type (Manager may add content)
        self.assertIn('id="faceted-add"', html)
        self.assertIn("++add++person?form.widgets.lastname=&amp;form.widgets.firstname=", html)
        self.assertIn('class="faceted-add-contact" href="http://nohost/plone/mydirectory/@@add-contact"', html)
        self.assertNotIn("faceted-add-organization", html)
        self.assertIn('<img src="http://nohost/plone/++resource++collective.contact.core/create_contact.png" />', html)
        # no result, add links with the searched text
        html = self.faceted_query(**{"type[]": "person", "texte[]": "Jean Dupont"})
        self.assertNotIn('class="contact-entry"', html)
        self.assertIn('id="msg-no-results"', html)
        self.assertIn("There is no contact matching your criteria.", html)
        self.assertNotIn("contacts-facetednav-batchactions", html)
        self.assertIn(
            'href="http://nohost/plone/mydirectory/++add++person?'
            'form.widgets.lastname=Dupont&amp;form.widgets.firstname=Jean"',
            html,
        )
        html = self.faceted_query(**{"type[]": "held_position", "texte[]": "Dupont"})
        self.assertIn("++add++person?form.widgets.lastname=Dupont&amp;form.widgets.firstname=", html)
        self.assertIn("faceted-add-contact", html)
        html = self.faceted_query(**{"type[]": "organization", "texte[]": "Navy Seal"})
        self.assertIn('href="http://nohost/plone/mydirectory/++add++organization?form.widgets.title=Navy+Seal"', html)
        self.assertNotIn("faceted-add-person", html)
        self.assertIn(
            '<img src="http://nohost/plone/++resource++collective.contact.core/organization_icon.png" />', html
        )
        self.assertNotIn("faceted-add-contact", html)
        # no add link for a user who may not add content
        setRoles(self.portal, TEST_USER_ID, ["Member", "Reader"])
        html = self.faceted_query(**{"type[]": "organization", "texte[]": ""})
        self.assertIn("Armée de terre", html)
        self.assertNotIn("faceted-add", html)

    @unittest.expectedFailure
    def test___call___add_links_prefill(self):
        """Plone 4 bug: the add forms ignore the values the "Create ..." links carry: z3c.form ignores
        form values sent by GET (Plone hotfix 20160830) and the organization title is form.widgets.IBasic.title"""
        for type_name, text, widget in (
            ("organization", "Navy", "IBasic.title"),
            ("person", "Jean Dupont", "lastname"),
        ):
            html = self.faceted_query(**{"type[]": type_name, "texte[]": text})
            url = html.split('class="faceted-add-%s" href="' % type_name)[1].split('"')[0].replace("&amp;", "&")
            path, query = url.replace("http://nohost/plone/", "").split("?")
            self.request.form.update(dict(param.split("=") for param in query.split("&")))
            add_form = self.portal.restrictedTraverse(str(path))
            add_form.update()
            self.assertEqual(add_form.form_instance.widgets[widget].value, text.split(" ")[-1])


class TestPreviewItem(IntegrationTestCase):
    """@@faceted-preview-item of person, organization, held_position"""

    def preview(self, obj):
        return obj.restrictedTraverse("@@faceted-preview-item")()

    def test___call__(self):
        self.request.set(ACTIONS_ENABLED_KEY, False)
        # person: title, phone, email, held positions with their phone/email when the person has none
        html = self.preview(self.directory.pepper)
        self.assertIn('class="contact-title">Mister Pepper</span>', html)
        self.assertIn("0288443344", html)
        self.assertIn('href="mailto:stephen.pepper@private.com"', html)
        self.assertIn('href="http://nohost/plone/mydirectory/pepper/sergent_pepper"', html)
        self.assertIn("Sergent de la brigade LH", html)
        self.assertIn('src="http://nohost/plone/++resource++collective.contact.core/defaultUser.png"', html)
        html = self.preview(self.directory.draper)
        self.assertIn("Capitaine de la division Alpha", html)
        self.assertIn("Division Beta", html)
        self.assertNotIn("contacts-facetednav-actions", html)
        # organization: title, phone, email
        html = self.preview(self.directory.armeedeterre)
        self.assertIn('class="organization-title">Armée de terre</span>', html)
        self.assertIn("01000000001", html)
        self.assertIn('href="mailto:contact@armees.fr"', html)
        # held position: full title, own phone and email
        html = self.preview(self.directory.pepper.sergent_pepper)
        self.assertIn("Mister Pepper, Sergent de la brigade LH", html)
        self.assertIn("0288552211", html)
        self.assertIn('href="mailto:sgt.pepper@armees.fr"', html)
        # contact actions when the actions are enabled
        self.request.set(ACTIONS_ENABLED_KEY, True)
        uid = self.directory.rambo.UID()
        html = self.preview(self.directory.rambo)
        self.assertIn('class="contacts-facetednav-actions"', html)
        self.assertIn('id="contact-action-edit-contact-%s"' % uid, html)
        self.assertIn('id="contact-action-delete-contact-%s"' % uid, html)


class TestJSONContacts(IntegrationTestCase):
    """@@json-contacts: all the results of the faceted query (no batch)"""

    def json_contacts(self, **form):
        self.request.form.update(form)
        return json.loads(self.directory.restrictedTraverse("@@json-contacts")())

    def test_query(self):
        view = self.directory.restrictedTraverse("@@json-contacts")
        # no criterion value (the default values are sent by javascript): all the contents
        # (the site root is a cataloged content on Plone 6)
        self.assertEqual(len(view.query()), len(api.content.find(context=self.portal)))
        # as sent by javascript: all the results, whatever the batch start and size
        self.request.form.update(
            {"type[]": "held_position", "b_start[]": "2", "resultsnum[]": "5", "sort[]": "sortable_title"}
        )
        brains = view.query()
        self.assertEqual(len(brains), 6)
        self.assertEqual(brains[0].getPath(), "/plone/mydirectory/degaulle/adt")
        self.request.form.update({"type[]": "organization", "cfn_select_all_max": "5"})
        # one more than the max: javascript knows the max is passed
        self.assertEqual(len(view.query()), 6)

    def test___call__(self):
        contacts = self.json_contacts(**{"type[]": "organization"})
        self.assertEqual(len(contacts), 7)
        self.assertEqual(
            contacts[0], {"id": self.directory.armeedeterre.UID(), "path": "/plone/mydirectory/armeedeterre"}
        )
        self.assertEqual(self.request.response.getHeader("Cache-Control"), "no-cache")
        self.assertEqual(self.request.response.getHeader("Pragma"), "no-cache")
        contacts = self.json_contacts(**{"type[]": "person", "texte[]": "Rambo"})
        self.assertEqual(contacts, [{"id": self.directory.rambo.UID(), "path": "/plone/mydirectory/rambo"}])
        self.assertEqual(self.json_contacts(**{"texte[]": "Nobody"}), [])

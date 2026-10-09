# -*- coding: utf-8 -*-
from collective.contact.facetednav.testing import IntegrationTestCase
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestContactPortalTypesVocabulary(IntegrationTestCase):

    def test___call__(self):
        factory = getUtility(IVocabularyFactory, "collective.contact.facetednav.vocabularies.ContactPortalTypes")
        vocabulary = factory(self.directory)
        self.assertEqual(
            [(term.value, term.token, term.title) for term in vocabulary],
            [
                ("organization", "organization", "Organizations"),
                ("held_position", "held_position", "Contacts"),
                ("person", "person", "Persons"),
            ],
        )
        self.assertEqual(vocabulary.getTerm("person").title.domain, "collective.contact.facetednav")
        # eea.facetednavigation calls it with a widget view: its context is used
        self.assertEqual(
            [term.value for term in factory(self.directory.restrictedTraverse("@@faceted_query"))],
            ["organization", "held_position", "person"],
        )

""" Types vocabularies
"""

from collective.contact.facetednav import _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class ContactPortalTypesVocabulary(object):
    """Vocabulary factory for contact portal types."""

    def __call__(self, context):
        context = getattr(context, "context", context)
        items = [(_("Organizations"), "organization"), (_("Contacts"), "held_position"), (_("Persons"), "person")]
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


ContactPortalTypesVocabularyFactory = ContactPortalTypesVocabulary()

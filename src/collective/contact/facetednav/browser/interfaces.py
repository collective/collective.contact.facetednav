from zope import schema
from zope.interface import Interface


class IContactFacetedSubtyper(Interface):
    """ Support for subtyping objects
    """

    actionsad = schema.Bool(u'Can enable contacts selection on faceted navigation')

    def can_enable_actions(self):
        """Enable selection
        """

    def can_disable_actions(self):
        """Enable selection
        """

    def enable_actions(self):
        """Enable selection
        """

    def disable_actions(self):
        """Enable selection
        """


class IContactPreviewItems(Interface):

    def update(self):
        pass

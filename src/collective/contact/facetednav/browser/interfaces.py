from zope import schema
from zope.interface import Interface


class IContactFacetedSubtyper(Interface):
    """ Support for subtyping objects
    """

    can_select = schema.Bool(u'Can enable contacts selection on faceted navigation')

    def can_enable_select(self):
        """Enable selection
        """

    def can_disable_select(self):
        """Enable selection
        """

    def enable_select(self):
        """Enable selection
        """

    def disable_select(self):
        """Enable selection
        """


class IContactPreviewItems(Interface):

    def update(self):
        pass

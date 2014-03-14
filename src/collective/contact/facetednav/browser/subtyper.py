""" Subtyping support
"""
from zope.interface import implements
from zope.interface import alsoProvides, noLongerProvides
from zope.publisher.interfaces import NotFound

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

from collective.contact.facetednav.browser.interfaces import IContactFacetedSubtyper
from collective.contact.facetednav.interfaces import ISelectableContacts
from collective.contact.facetednav import _


class ContactFacetedPublicSubtyper(BrowserView):
    """ Public support for subtyping objects
        view for non IPossibleFacetedNavigable objects
    """
    implements(IContactFacetedSubtyper)

    def _redirect(self, msg=''):
        """ Redirect
        """
        if self.request:
            if msg:
                IStatusMessage(self.request).addStatusMessage(msg, type='info')
            self.request.response.redirect(self.context.absolute_url())
        return msg

    @property
    def can_select(self):
        return ISelectableContacts.providedBy(self.context)

    def can_enable_select(self):
        """Can enable selection
        """
        return False

    def can_disable_select(self):
        """Can disable selection
        """
        return False

    def enable_select(self):
        """Enable selection
        """
        raise NotFound(self.context, 'enable_select', self.request)

    def disable_select(self):
        """Disable selection
        """
        raise NotFound(self.context, 'disable_select', self.request)


class ContactFacetedSubtyper(ContactFacetedPublicSubtyper):
    """ Support for subtyping objects
        view for IPossibleFacetedNavigable objects
    """

    def can_enable_select(self):
        """ See IFacetedSubtyper
        """
        return not self.can_select

    def can_disable_select(self):
        """ See IFacetedSubtyper
        """
        return self.can_select

    def enable_select(self):
        """ See IFacetedSubtyper
        """
        if not self.can_enable_select():
            return self._redirect('Faceted navigation not supported')
        alsoProvides(self.context, ISelectableContacts)

        self._redirect(_('Contacts selection enabled'))

    def disable_select(self):
        """ See IFacetedSubtyper
        """
        noLongerProvides(self.context, ISelectableContacts)
        self._redirect(_('Contacts selection disabled'))

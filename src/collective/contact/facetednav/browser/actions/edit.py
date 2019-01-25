from collective.contact.facetednav.browser.actions.base import ActionBase
from plone import api

from zope.i18nmessageid.message import MessageFactory
PMF = MessageFactory('plone')


class EditAction(ActionBase):

    klass = 'edit-contact'
    name = 'edit-contact'
    title = PMF(u"Edit")
    weight = 200

    @property
    def icon(self):
        return api.portal.get().absolute_url() + "/++resource++collective.contact.core/edit.png"

    def url(self):
        return "%s/edit" % self.context.absolute_url()

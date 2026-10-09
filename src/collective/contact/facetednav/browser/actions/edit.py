from collective.contact.facetednav.browser.actions.base import ActionBase
from zope.i18nmessageid.message import MessageFactory


PMF = MessageFactory("plone")


class EditAction(ActionBase):

    klass = "edit-contact"
    name = "edit-contact"
    icon = "plone-edit"
    title = PMF("Edit")
    weight = 200

    def url(self):
        return "%s/edit" % self.context.absolute_url()

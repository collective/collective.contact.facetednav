from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.contact.facetednav.browser.view import json_output
from collective.contact.facetednav.browser.batchactions.base import ActionBase
from collective.contact.facetednav import _


class DeleteAction(ActionBase):

    label = _("Delete selected contacts")
    name = 'delete'
    klass = 'destructive'
    onclick = 'contactfacetednav.delete_selection()'


class DeleteSelection(BrowserView):

    @json_output
    def delete(self):
        uids = self.request['uids']
        ctool = getToolByName(self.context, 'portal_catalog')
        mtool = getToolByName(self.context, 'portal_membership')
        brains = ctool(UID=uids)
        fails = []
        for b in brains:
            obj = b.getObject()
            if mtool.checkPermission('Delete objects', obj):
                parent = obj.getParentNode()
                parent.manage_delObjects([obj.getId()])
            else:
                fails.append(b.getPath())

        return fails
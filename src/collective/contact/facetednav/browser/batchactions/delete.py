from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from collective.contact.facetednav.browser.view import json_output
from collective.contact.facetednav.browser.batchactions.base import ActionBase
from collective.contact.facetednav import _
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo
from zope.i18n import translate
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException


class DeleteAction(ActionBase):

    label = _("Delete selected contacts")
    name = 'delete'
    klass = 'destructive'

    @property
    def onclick(self):
        return 'contactfacetednav.delete_selection("%s")' % translate(
                    _('confirm_delete_selection',
                      default=u"Are you sure you want to remove $num selected content(s) ?"))


class DeleteSelection(BrowserView):

    @json_output
    def delete(self):
        uids = self.request['uids']
        ctool = getToolByName(self.context, 'portal_catalog')
        mtool = getToolByName(self.context, 'portal_membership')
        brains = ctool(UID=uids)
        fails = []
        success = 0
        integrity_info = ILinkIntegrityInfo(self.request)
        for b in brains:
            obj = b.getObject()
            integrity_info.addDeletedItem(obj)
            if not mtool.checkPermission('Delete objects', obj):
                fails.append(translate(_(u"Unauthorized: ${path}",
                                         mapping={'path': b.getPath()}),
                                       context=self.request))
            else:
                try:
                    parent = obj.getParentNode()
                    parent.manage_delObjects([obj.getId()])
                except LinkIntegrityNotificationException:
                    pass
                finally:
                    success += 1

        IStatusMessage(self.request).add(_("msg_objects_deleted",
                                           default="${num} object(s) deleted",
                                           mapping={'num': success}))
        if fails:
            IStatusMessage(self.request).add(
                      _("msg_objects_delete_failed",
                        default="${num} object(s) were not deleted : ${fails}",
                        mapping={'num': len(fails), 'fails': ", ".join(fails)}),
                      'error')


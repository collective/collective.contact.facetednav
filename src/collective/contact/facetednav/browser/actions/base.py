from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class BatchActionBase(ViewletBase):
    index = ViewPageTemplateFile('batchaction.pt')
    klass = 'context'
    onclick = None
    name = None


class ActionBase(ViewletBase):
    index = ViewPageTemplateFile('action.pt')
    klass = None
    onclick = None
    icon = None
    name = None
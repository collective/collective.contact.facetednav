from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class ActionBase(ViewletBase):
    index = ViewPageTemplateFile('batchaction.pt')
    klass = 'context'
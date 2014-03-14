from zope.interface import implements
from zope.viewlet.interfaces import IViewletManager
from zope.viewlet.manager import ConditionalViewletManager


class IBatchActions(IViewletManager):
    pass

class BatchActionsViewletManager(ConditionalViewletManager):
    implements(IBatchActions)


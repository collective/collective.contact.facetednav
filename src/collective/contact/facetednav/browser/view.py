from json.encoder import JSONEncoder

from Products.CMFPlone.utils import safe_hasattr
from Products.Five import BrowserView

from eea.facetednavigation.browser.app.query import FacetedQueryHandler

from collective.contact.facetednav.interfaces import IActionsEnabled
from plone import api


class PreviewItem(BrowserView):
    def use_view(self):
        ptype = self.context.portal_type
        proptools = api.portal.get_tool('portal_properties')
        if safe_hasattr(proptools, 'site_properties') \
                and safe_hasattr(proptools.site_properties, 'typesUseViewActionInListings'):
            return ptype in proptools.site_properties.typesUseViewActionInListings
        else:
            return ptype in api.portal.get_registry_record('plone.types_use_view_action_in_listings')


ACTIONS_ENABLED_KEY = 'collective.contact.facetednav.actions_enabled'

class ContactsFacetedQueryHandler(FacetedQueryHandler):

    def actions_enabled(self):
        enabled = IActionsEnabled.providedBy(self.context)
        self.request.set(ACTIONS_ENABLED_KEY, enabled)
        return enabled


def json_output(method):

    def json_method(*arg, **kwargs):
        value = method(*arg, **kwargs)
        return JSONEncoder().encode(value)

    return json_method


class JSONContacts(FacetedQueryHandler):
    """JSON view that gets with all values without batch in json
    """

    def query(self, batch=True, sort=True, **kwargs):
        """ Search using given criteria
        """
        if self.request:
            kwargs.update(self.request.form)

        kwargs = dict((key.replace('[]', ''), val)
                      for key, val in kwargs.items())

        kwargs.pop('sort', None)
        kwargs.pop('batch', None)
        kwargs.pop('b_start', None)
        faceted_query_view = self.context.unrestrictedTraverse('@@faceted_query')
        brains = faceted_query_view.query(batch=False, sort=False, **kwargs)
        return brains

    @json_output
    def __call__(self, *args, **kwargs):
        self.request.RESPONSE.setHeader('Cache-Control', 'no-cache')
        self.request.RESPONSE.setHeader('Pragma', 'no-cache')
        self.brains = self.query(**kwargs)
        infos = []
        for brain in self.brains:
            info = {'id': brain.UID,
                    'path': brain.getPath()}
            infos.append(info)

        return infos

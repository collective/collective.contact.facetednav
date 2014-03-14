from json.encoder import JSONEncoder

from Products.Five import BrowserView

from eea.facetednavigation.browser.app.query import FacetedQueryHandler

from collective.contact.facetednav.interfaces import ISelectableContacts


IS_SELECTABLE_KEY = 'collective.contact.facetednav.is_selectable'

class PreviewItem(BrowserView):
    pass


class ContactsFacetedQueryHandler(FacetedQueryHandler):

    def is_selectable(self):
        return ISelectableContacts.providedBy(self.context)


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
        self.brains = self.query(**kwargs)
        infos = []
        for brain in self.brains:
            info = {'id': brain.UID}
            infos.append(info)

        return infos
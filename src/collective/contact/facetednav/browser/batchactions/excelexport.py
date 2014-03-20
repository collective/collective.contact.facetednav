from collective.contact.facetednav.browser.batchactions.base import ActionBase
from collective.contact.facetednav import _


class ExcelExportAction(ActionBase):

    label = _("Excel export")
    name = 'excelexport'
    klass = 'context'

    @property
    def onclick(self):
        return 'contactfacetednav.excel_export()'
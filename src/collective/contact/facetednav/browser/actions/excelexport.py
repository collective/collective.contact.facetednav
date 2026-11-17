from collective.contact.facetednav import _
from collective.contact.facetednav.browser.actions.base import BatchActionBase


class ExcelExportAction(BatchActionBase):

    label = _("Excel export")
    name = "excelexport"
    klass = "context"
    weight = 800

    @property
    def onclick(self):
        return "contactfacetednav.excel_export()"

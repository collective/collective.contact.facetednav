# -*- coding: utf-8 -*-
from collective.contact.facetednav.browser.actions.excelexport import ExcelExportAction
from collective.contact.facetednav.testing import IntegrationTestCase


class TestExcelExportAction(IntegrationTestCase):
    """registered when collective.excelexport is installed (dependency of collective.documentgenerator)"""

    def setUp(self):
        super(TestExcelExportAction, self).setUp()
        manager = self.viewlet_manager("collective.contact.facetednav.batchactions", self.directory, "@@faceted_query")
        self.viewlet = manager.viewlets[1]

    def test_onclick(self):
        self.assertIsInstance(self.viewlet, ExcelExportAction)
        self.assertEqual(self.viewlet.onclick, "contactfacetednav.excel_export()")

    def test_render(self):
        html = self.viewlet.render()
        self.assertIn('id="contact-facetednav-action-excelexport"', html)
        self.assertIn('class="context"', html)
        self.assertIn('value="Excel export"', html)
        self.assertIn('onclick="contactfacetednav.excel_export()"', html)

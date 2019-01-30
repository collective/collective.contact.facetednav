try:
    from Products.CMFPlone.resources.browser.cook import cookWhenChangingSettings
except ImportError:
    cookWhenChangingSettings = None

from ecreall.helpers.upgrade.interfaces import IUpgradeTool


def v2(context):
    tool = IUpgradeTool(context)
    tool.runProfile('collective.contact.facetednav.upgrades:v2')


def v3(context):
    tool = IUpgradeTool(context)
    tool.runImportStep('collective.contact.facetednav', 'actions')
    tool.runImportStep('collective.contact.facetednav', 'jsregistry')


def v4(context):
    tool = IUpgradeTool(context)
    tool.refreshResources()


def v5(context):
    tool = IUpgradeTool(context)
    tool.runImportStep('collective.contact.core', 'cssregistry')
    tool.runImportStep('collective.contact.core', 'jsregistry')
    tool.runImportStep('collective.contact.core', 'plone.app.registry')
    tool.refreshResources()
    if cookWhenChangingSettings is not None:
        cookWhenChangingSettings(context)

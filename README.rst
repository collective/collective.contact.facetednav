=============================
collective.contact.facetednav
=============================

Faceted navigation view for collective.contact.core directory.

Read eea.facetednavigation and collective.contact.core documentation
for more information about those amazing products.

This faceted navigation has a pluggable and optional feature that allows user
to apply actions to contacts and  batch actions to select contacts.
You have to "Enable actions" on directory actions.

By default, you have a "delete" action (with selection) and an "edit" action.
If you have installed collective.excelexport, you also have an excel export button.

You can add new actions, adding viewlets to collective.contact.facetednav.batchactions
viewlet manager (collective.contact.facetednav.batchactions.manager.IBatchActions interface)
and to collective.contact.facetednav.actions manager (collective.contact.facetednav.batchactions.manager.IActions interface)
You have to write the javascript code to handle it.

Some api will help you to handle the list of selected contents uids and pathes.
Use delete action as a model.
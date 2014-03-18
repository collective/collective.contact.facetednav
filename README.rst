=============================
collective.contact.facetednav
=============================

Faceted navigation view for collective.contact.core directory.

Read eea.facetednavigation and collective.contact.core documentation
for more information about those amazing products.

This faceted navigation has a pluggable and optional feature that allows user
to select contacts and apply batch actions on them.
You have to "Enable contacts selection" on directory actions.
By default, you have a "delete" action.

You can add new actions, adding viewlets to collective.contact.facetednav.batchactions
viewlet manager (collective.contact.facetednav.batchactions.manager.IBatchActions interface)
You have to write the javascript code to handle it.
Some api will help you to handle the list of selected contents uids and pathes.
Use delete action as a model.
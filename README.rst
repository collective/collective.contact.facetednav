=============================
collective.contact.facetednav
=============================

This add-on is part of the ``collective.contact.*`` suite. For an overview and a demo of these suite, see `collective.contact.demo <https://github.com/collective/collective.contact.demo>`__.

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
See collective.contact.facetednav.browser.actions.base abstract classes.

Some api will help you to handle the list of selected contents uids and pathes.
Use delete action as a model.


Installation
============

* Add collective.contact.facetednav to your eggs.
* Add collective.contact.facetednav to your zcml. #It is not auto included#.
* Re-run buildout.
* Install the product in your plone site. It installs eea.facetednavigation if it is not already installed.

If you don't want all default features, include only minimal.zcml file and
the files you want in configure.zcml.


IMPORTANT : Compatibility with collective.js.jqueryui
-----------------------------------------------------

collective.js.jqueryui is a dependency of eea.
For now, collective.js.jqueryui is not compatible with plone.formwidget.autocomplete,
which is a dependency of collective.contact.core.
You **must** disable jqueryui autocomplete feature if you want contact widget to work.
You can disable the plugin in the JQuery UI configurations settings of site control panel.


Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://secure.travis-ci.org/collective/collective.contact.facetednav.png
    :target: http://travis-ci.org/collective/collective.contact.facetednav

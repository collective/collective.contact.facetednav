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
See collective.contact.facetednav.browser.actions.base abstract classes for more documentation.

Some api will help you to handle the list of selected contents uids and pathes.
Use delete action as a model.

You can set the maximum value of selectable items.
Set for instance in your custom javascript:

    contactfacetednav.SELECT_ALL_MAX = 1000;


Installation
============

* Add collective.contact.facetednav to your eggs.
* Add collective.contact.facetednav to your zcml. #It is not auto included#.
* Re-run buildout.
* Install the product in your plone site.

If you don't want all default features, include only minimal.zcml file and
the files you want in configure.zcml.


Translations
============

This product has been translated into

- German.

- Spanish.

- French.

- Italian.

- Slovenian.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.contact.facetednav/issues
- Source Code: https://github.com/collective/collective.contact.facetednave
- Documentation: https://github.com/collective/collective.contact.demo/blob/master/README.md

.. _`opening a ticket`: https://github.com/collective/collective.contact.facetednav/issues


Tests
=====

This add-on is tested using Travis CI. The current status of the add-on is :

.. image:: https://img.shields.io/travis/collective/collective.contact.facetednav/master.svg
    :target: http://travis-ci.org/collective/collective.contact.facetednav

.. image:: http://img.shields.io/pypi/v/collective.contact.facetednav.svg
    :target: https://pypi.python.org/pypi/collective.contact.facetednav


License
=======

The project is licensed under the GPLv2.

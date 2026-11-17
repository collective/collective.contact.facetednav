/* Selection and actions of the contacts of a faceted directory.
 * Classic script deferred after eea.facetednavigation's faceted.view bundle: contactfacetednav stays global
 * (collective.contact.duplicated, collective.contact.contactlist use it). */
var contactfacetednav = {};

contactfacetednav.SELECT_ALL_MAX = 0;
contactfacetednav.selector = '.contact-entry .contact-selection input';
contactfacetednav.status_messages = null;
// links of the results opened in a modal; a saved form refreshes the results instead of reloading the page
contactfacetednav.modal_links = '.edit-contact, .delete-contact, #faceted-add a.faceted-add-organization, #faceted-add a.faceted-add-contact';
contactfacetednav.modal_options = {actionOptions: {displayInModal: false, reloadWindowOnClose: false}};

/* A contact of the results ({id: uid, path: path}), API of the Plone 4 Backbone model */
contactfacetednav.Contact = function (attributes) {
    this.attributes = jQuery.extend({selected: false}, attributes);
    this.id = this.attributes.id;
};

contactfacetednav.Contact.prototype = {
    get: function (name) {
        return this.attributes[name];
    },
    setSelected: function (value) {
        this.attributes.selected = value;
        this.render();
        contactfacetednav.contacts.render();
    },
    isSelected: function () {
        return this.attributes.selected;
    },
    getPath: function () {
        return this.attributes.path;
    },
    render: function () {
        // its checkbox, if it is in the current page
        jQuery('#contact-' + this.id).prop('checked', this.isSelected()).trigger('change');
    }
};

/* All the contacts of the faceted query, not only the current page, API of the Plone 4 Backbone collection */
contactfacetednav.Contacts = function () {
    var self = this;
    this.models = [];
    this.length = 0;
    jQuery.getJSON(this.url(), function (contacts) {
        self.models = contacts.map(function (attributes) {
            return new contactfacetednav.Contact(attributes);
        });
        self.length = self.models.length;
        self.each(function (contact) {
            contact.render();
        });
        self.render();
    });
};

contactfacetednav.Contacts.prototype = {
    url: function () {
        var max = contactfacetednav.SELECT_ALL_MAX ? '&cfn_select_all_max=' + contactfacetednav.SELECT_ALL_MAX : '';
        return jQuery('body').data('base-url') + '/json-contacts?' + jQuery.param(Faceted.SortedQuery()) + max;
    },
    each: function (callback) {
        this.models.forEach(callback);
    },
    get: function (id) {
        return this.models.find(function (contact) {
            return contact.id === id;
        });
    },
    setSelectedAll: function (value) {
        this.each(function (contact) {
            contact.attributes.selected = value;
            contact.render();
        });
        this.render();
    },
    selectAll: function () {
        this.setSelectedAll(true);
    },
    unselectAll: function () {
        this.setSelectedAll(false);
    },
    selection: function () {
        return this.models.filter(function (contact) {
            return contact.isSelected();
        });
    },
    selection_uids: function () {
        return this.selection().map(function (contact) {
            return contact.id;
        });
    },
    selection_pathes: function () {
        return this.selection().map(function (contact) {
            return contact.getPath();
        });
    },
    hasSelection: function () {
        return this.selection().length > 0;
    },
    render: function () {
        // buttons: multiple-selection ones need 2 contacts, global-selection ones no selection
        var count = this.selection().length;
        var select_all = jQuery('#contacts-selectall');
        var label = select_all.attr(count ? 'data-unselect-all-msg' : 'data-select-all-msg');
        var too_large = count === 0 && this.resultTooLargeForSelectAll();
        jQuery('.contacts-buttons input').prop('disabled', count === 0);
        jQuery('.contacts-buttons input.multiple-selection').prop('disabled', count < 2);
        jQuery('.contacts-buttons input.global-selection').prop('disabled', count > 0);
        select_all.attr('value', label).prop('disabled', too_large).attr('title', too_large ?
            select_all.attr('data-select-all-too-large-msg') + ' (> ' + contactfacetednav.SELECT_ALL_MAX + ')' : label);
        jQuery('#contacts-selection-num .num').text(count);
    },
    resultTooLargeForSelectAll: function () {
        return !!contactfacetednav.SELECT_ALL_MAX && this.length > contactfacetednav.SELECT_ALL_MAX;
    }
};

contactfacetednav.init = function () {
    jQuery(document).on('click', '#contacts-selectall', function () {
        if (contactfacetednav.contacts.hasSelection()) {
            contactfacetednav.contacts.unselectAll();
        } else {
            contactfacetednav.contacts.selectAll();
        }
    });
    jQuery(document).on('click', contactfacetednav.selector, function () {
        contactfacetednav.contacts.get(this.id.split('-')[1]).setSelected(this.checked);
    });

    // bound before Faceted.Load's handler, which resets Faceted.b_start_changed;
    // namespaced so that an other module can unbind it
    jQuery(Faceted.Events).on(Faceted.Events.AJAX_QUERY_SUCCESS + '.rendercheckboxes', function () {
        if (!jQuery('#contacts-facetednav-batchactions').length) {
            return;
        }
        // the selection is kept when changing page
        if (!Faceted.b_start_changed || !contactfacetednav.contacts) {
            contactfacetednav.contacts = new contactfacetednav.Contacts();
        }
        contactfacetednav.contacts.each(function (contact) {
            contact.render();
        });
        contactfacetednav.contacts.render();
        contactfacetednav.show_messages();
    });

    jQuery(Faceted.Events).on(Faceted.Events.AJAX_QUERY_SUCCESS, function () {
        // the class and options for Plone's first pattern scan, patPloneModal for the results loaded after it
        var links = jQuery('#faceted-results').find(contactfacetednav.modal_links)
            .addClass('pat-plone-modal')
            .attr('data-pat-plone-modal', JSON.stringify(contactfacetednav.modal_options))
            .on('formActionSuccess.plone-modal.patterns', function () {
                Faceted.Form.do_form_query();
            });
        if (jQuery.fn.patPloneModal) {
            links.patPloneModal();
        }
    });
};

contactfacetednav.store_overlay_messages = function (el) {
    contactfacetednav.status_messages = jQuery(el).find('.portalMessage');
};

contactfacetednav.show_messages = function () {
    if (contactfacetednav.status_messages !== null) {
        jQuery('#contacts-facetednav-batchactions').prepend(contactfacetednav.status_messages);
        contactfacetednav.status_messages = null;
    }
};

contactfacetednav.serialize_uids = function (uids) {
    /* Helpers to prepare sending uids list the more convenient way
     */
    return jQuery.param({'uids:list': uids}, true);
};

contactfacetednav.serialize_pathes = function (pathes) {
    /* Helpers to prepare sending pathes list the more convenient way
     */
    return jQuery.param({'pathes:list': pathes}, true);
};

contactfacetednav.delete_selection = function (confirm_msg) {
    var uids = contactfacetednav.contacts.selection_uids();
    if (confirm(confirm_msg.replace('$num', uids.length))) {
        // CSRF token of plone.protect
        var token = jQuery('#protect-script').attr('data-token') || jQuery('input[name="_authenticator"]').val();
        jQuery.post(
            jQuery('body').data('base-url') + '/delete_selection',
            contactfacetednav.serialize_uids(uids) + '&' + jQuery.param({_authenticator: token}),
            function () {
                Faceted.Form.do_form_query();
            }
        );
    }
};

contactfacetednav.excel_export = function () {
    var uids = contactfacetednav.contacts.selection_uids();
    var url = jQuery('body').data('portal-url') + '/@@collective.excelexport?excelexport.policy=excelexport.search';
    var form = jQuery('<form action="' + url + '" method="post"></form>');

    for (var num in uids) {
        form.append('<input type="hidden" name="UID:list" value="' + uids[num] + '" />');
    }
    jQuery('body').append(form);
    form.submit();
    form.remove();
};

contactfacetednav.init();

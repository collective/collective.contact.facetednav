var contactfacetednav = {};

contactfacetednav.SELECT_ALL_MAX = 0;

contactfacetednav.selectionchange = jQuery.Event('selectionchange');
contactfacetednav.selector = '.contact-entry .contact-selection input';

contactfacetednav.init = function() {
    contactfacetednav.status_messages = null;
    Backbone.emulateHTTP = true;
    Backbone.emulateJSON = true;
    jQuery('body').on('click', '#contacts-selectall', function() {
        if(contactfacetednav.contacts.selection().length > 0){
            contactfacetednav.contacts.unselectAll();
        } else {
            contactfacetednav.contacts.selectAll();
        }
    });

    // use a namespace here so we can unbind the callback in an other module
    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS + '.rendercheckboxes', function() {
        jQuery('#contacts-facetednav-batchactions').each(function(){
            if (!Faceted.b_start_changed) {
                contactfacetednav.contacts = new contactfacetednav.Contacts();
            } else {
                contactfacetednav.contacts.each(function(contact) {
                    contact.render();
                });
            }
            window.setTimeout(function() {
                contactfacetednav.contacts.render();
            }, 0);
            jQuery(contactfacetednav.selector).click(function() {
                var input = jQuery(this);
                var uid = input.attr('id').split('-')[1];
                var contact = contactfacetednav.contacts.get(uid);
                var selected = input.prop('checked');
                contact.setSelected(selected);
                contact.render();
            });
            contactfacetednav.show_messages();
        });
    });
    jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function() {
        jQuery('#faceted-add a.faceted-add-organization').prepOverlay({
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: '#form',
            closeselector: '[name="form.buttons.cancel"]',
            noform: function(el, pbo) {
                Faceted.Form.do_form_query();
                return 'close';},

        });
        jQuery('#faceted-add a.faceted-add-contact').prepOverlay({
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: '#oform',
            closeselector: '[name="oform.buttons.cancel"]',
            noform: function(el, pbo) {
                Faceted.Form.do_form_query();
                return 'close';},
        });
    });
};

contactfacetednav.store_overlay_messages = function(el){
    contactfacetednav.status_messages = jQuery(el).find('.portalMessage');
};

contactfacetednav.show_messages = function(){
    if(contactfacetednav.status_messages !== null){
        jQuery('#contacts-facetednav-batchactions').prepend(contactfacetednav.status_messages);
        contactfacetednav.status_messages = null;
    }
};

contactfacetednav.Contact = Backbone.Model.extend({

    defaults : {
        id : "?????????????????",
        path : "?????????????????",
        selected : false,
    },

    initialize : function Contact() {
        this.bind('change', this.render);
    },

    setSelected : function(value) {
        this.set({
            'selected' : value
        });
    },

    isSelected : function() {
        return this.get('selected');
    },

    getPath : function() {
        return this.get('path');
    },

    render : function() {
        var input = jQuery('#contact-' + this.get('id'));
        if (input.length === 0) {
            // Not in current page
            return;
        }
        else if (this.isSelected()) {
            input.prop('checked', true);
            input.trigger('change');
        }
        else{
            input.prop('checked', false);
            input.trigger('change');
        }

    }
});

contactfacetednav.Contacts = Backbone.Collection.extend({
    model : contactfacetednav.Contact,
    initialize : function() {
        this.bind('change', this.render);
        this.fetch({
            success : function(model, response) {
                model.each(function(contact) {
                    contact.render();
                });
            }
        });
    },
    url : function() {
        var baseURL = $('base').attr('href');
        var selectAllMaxParam = contactfacetednav.SELECT_ALL_MAX ? '&cfn_select_all_max=' + contactfacetednav.SELECT_ALL_MAX : ''
        return baseURL + '/json-contacts?' + jQuery.param(Faceted.SortedQuery()) + selectAllMaxParam;
    },
    selectAll: function(){
        this.off('change', this.render);
        this.each(function(contact){
            contact.setSelected(true);
        });
        this.render();
        this.on('change', this.render);
        this.trigger('select-all');
    },
    unselectAll: function(){
        this.off('change', this.render);
        this.each(function(contact){
            contact.setSelected(false);
        });
        this.render();
        this.on('change', this.render);
        this.trigger('unselect-all');
    },
    selection: function(){
        return this.filter(function(contact){
            return contact.isSelected();
        });
    },
    selection_uids: function(){
        var uids = [];
        var selection = this.selection();
        for(var num in selection){
            uids.push(selection[num].id);
        }
        return uids;
    },
    selection_pathes: function(){
        var uids = [];
        var selection = this.selection();
        for(var num in selection){
            uids.push(selection[num].getPath());
        }
        return uids;
    },
    hasSelection: function(){
        return this.selection().length > 0;
    },
    render: function(){
        var selection_length = this.selection().length;
        var select_all_button = jQuery('#contacts-selectall');

        if(selection_length===0){
            jQuery('.contacts-buttons input').attr('disabled', true);
            jQuery('.contacts-buttons input.global-selection').attr('disabled', false);
            select_all_button.attr('title', select_all_button.attr('data-select-all-msg'));
            select_all_button.attr('value', select_all_button.attr('data-select-all-msg'));

            if (this.resultTooLargeForSelectAll()) {
                var too_large_msg = select_all_button.attr('data-select-all-too-large-msg') + ' (> ' + contactfacetednav.SELECT_ALL_MAX + ')';
                select_all_button.attr('title', too_large_msg);
                select_all_button.attr('disabled', true);
            } else {
                select_all_button.attr('disabled', false);
            }
        }
        else if(selection_length===1){
            jQuery('.contacts-buttons input').attr('disabled', false);
            jQuery('.contacts-buttons input.multiple-selection').attr('disabled', true);
            jQuery('.contacts-buttons input.global-selection').attr('disabled', true);
            select_all_button.attr('disabled', false);
            select_all_button.attr('title', select_all_button.attr('data-unselect-all-msg'));
            select_all_button.attr('value', select_all_button.attr('data-unselect-all-msg'));
        }
        else{
            jQuery('.contacts-buttons input').attr('disabled', false);
            jQuery('.contacts-buttons input.global-selection').attr('disabled', true);
            select_all_button.attr('disabled', false);
            select_all_button.attr('title', select_all_button.attr('data-unselect-all-msg'));
            select_all_button.attr('value', select_all_button.attr('data-unselect-all-msg'));
        }
        jQuery('#contacts-selection-num .num').text(selection_length);

    },
    resultTooLargeForSelectAll: function() {
        return !!contactfacetednav.SELECT_ALL_MAX && this.length > contactfacetednav.SELECT_ALL_MAX;
    }
});


jQuery(document).ready(contactfacetednav.init);

contactfacetednav.serialize_uids = function(uids){
    /* Helpers to prepare sending uids list the more convenient way
     */
    return jQuery.param({'uids:list': uids}, true);
};

contactfacetednav.serialize_pathes = function(pathes){
    /* Helpers to prepare sending pathes list the more convenient way
     */
    return jQuery.param({'pathes:list': pathes}, true);
};

contactfacetednav.delete_selection = function(confirm_msg){
    var uids = contactfacetednav.contacts.selection_uids();
    confirm_msg = confirm_msg.replace('$num', uids.length);
    if(confirm(confirm_msg)){
        var base_url = jQuery('base').attr('href');
        jQuery.post(
            base_url + '/delete_selection',
            contactfacetednav.serialize_uids(uids),
            function(response){
                // response can be HTML from link integrity page
                if (response && response.status !== 'success') {
                    // display link integrity overlay
                    var divOverlay = $('<div class="overlay overlay-ajax"></div>').appendTo('body');
                    var divPbAjax = $('<div class="pb-ajax"></div>').appendTo(divOverlay);
                    var div = $('<div></div>').appendTo(divPbAjax);
                    var linkIntegrityHTML = $('<div></div>').html(response);
                    var content = $(linkIntegrityHTML).find('#content');
                    div.html(content);
                    var width = document.body.clientWidth * 0.8;
                    var right = document.body.clientWidth / 2 - width / 2;
                    divOverlay.css({
                        display: 'block',
                        position: 'absolute',
                        right: right + 'px',
                        top: '200px',
                        width: width + 'px',
                        zIndex: 9999,
                    });
                    var form = divOverlay.find('form');

                    // hide delete button as it has no meaning here
                    form.find('input[name=delete]').hide();

                    var params = form.serialize();
                    form.find('input').click(function (e) {
                        form.button = e.target.name;
                    });
                    form.submit(function(e) {
                        e.preventDefault();
                        params = params + '&' + form.button + '="clicked"';
                        $.post(form.attr('action'), params, function(result) {
                            window.location.reload(true);
                        });
                    });
                } else {
                    // success
                    Faceted.Form.do_form_query();
                }
            }
        );
    }
};

contactfacetednav.excel_export = function(){
    var uids = contactfacetednav.contacts.selection_uids();
    var url = portal_url + '/@@collective.excelexport?excelexport.policy=excelexport.search';
    var form = jQuery('<form action="' + url + '" method="post"></form>');

    for(var num in uids){
        form.append('<input type="hidden" name="UID:list" value="' + uids[num] + '" />');
    }
    jQuery('body').append(form);
    form.submit();
    form.remove();
};

jQuery(Faceted.Events).bind(Faceted.Events.AJAX_QUERY_SUCCESS, function(){
    jQuery('#faceted-results .delete-contact').each(function(){
        var link = jQuery(this);
        link.prepOverlay({
                subtype: 'ajax',
                filter: common_content_filter,
                formselector: '#delete_confirmation',
                closeselector: '[name="cancel"]',
                noform: function(el, pbo) {
                    Faceted.Form.do_form_query();
                    return 'close';},
              });
    });
    jQuery('#faceted-results .edit-contact').each(function(){
        var link = jQuery(this);
        link.prepOverlay({
                subtype: 'ajax',
                filter: common_content_filter,
                formselector: '#form',
                closeselector: '[name="form.button.cancel"]',
                noform: function(el, pbo) {
                    Faceted.Form.do_form_query();
                    return 'close';},
              });
    });
});

*** Settings ***
Documentation  collective.contact.facetednav keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.0 syntax (shared with the Plone 4.3 environment).
...            Fixture: collective.contact.core test data; mydirectory is a faceted navigation
...            (tests/contacts-faceted.xml: text search "texte", radio "type", default organization).
...            Selectors: this package (query.pt, preview-*.pt, actions/*.pt) and eea.facetednavigation widgets.
Resource  ui_plone${PLONE_MAJOR}.robot


*** Variables ***
${DIRECTORY_URL}  ${PLONE_URL}/mydirectory
${RESULTS}  css=#faceted-results
${BATCH_ACTIONS}  css=#contacts-facetednav-batchactions
${SELECT_ALL}  css=#contacts-selectall
${SELECTION_NUM}  css=#contacts-selection-num .num


*** Keywords ***
Open a manager browser
    Open test browser
    Set window size  1280  2000
    Enable autologin as  Manager

Uid of
    [Documentation]  uid of a content of mydirectory, by path (e.g. degaulle/adt)
    [Arguments]  ${path}
    ${uid}=  Path to uid  /${PLONE_SITE_ID}/mydirectory/${path}
    [Return]  ${uid}

Enable the contact actions
    [Documentation]  "Enable actions" item of the Actions menu (Plone 6: its URL carries the _authenticator)
    Open the faceted directory
    Click the content action  faceted.actions.enable
    The status message contains  Contacts actions enabled

Open the faceted directory
    Go to  ${DIRECTORY_URL}
    The results show  Armée de terre
    The faceted query is done

Show the contacts of type
    [Documentation]  organization, held_position or person (radio of the "type" criterion)
    [Arguments]  ${type}
    The faceted query is done
    Click element  css=#type_${type}

Search the text
    [Arguments]  ${text}
    The faceted query is done
    Input text  css=#texte  ${text}
    Click button  css=#texte_button

The faceted query is done
    [Documentation]  eea.facetednavigation locks the page (overlay) during a query
    Wait until element is not visible  css=.faceted-lock-overlay

The results show
    [Arguments]  ${text}
    Wait until element contains  ${RESULTS}  ${text}

The results do not show
    [Arguments]  ${text}
    Wait until keyword succeeds  10s  0.5s  Element should not contain  ${RESULTS}  ${text}

The no result message is shown
    Wait until element is visible  css=#msg-no-results

The contacts have a selection box
    Wait until page contains element  ${RESULTS} .contact-selection input[type="checkbox"]
    Page should contain element  ${BATCH_ACTIONS}

The contacts have no selection box
    Wait until page contains element  ${RESULTS} .contact-entry
    Page should not contain element  ${RESULTS} .contact-selection input
    Page should not contain element  ${BATCH_ACTIONS}

Select the contact
    [Documentation]  once the contacts of the results are loaded (backbone collection, json-contacts)
    [Arguments]  ${path}
    ${uid}=  Uid of  ${path}
    Wait for condition  return typeof contactfacetednav.contacts !== 'undefined' && contactfacetednav.contacts.get('${uid}') !== undefined
    Click element  css=#contact-${uid}

The selected contacts number is
    [Arguments]  ${num}
    Wait until element contains  ${SELECTION_NUM}  ${num}

The batch action is enabled
    [Arguments]  ${name}
    Wait until element is enabled  css=#contact-facetednav-action-${name}

The batch action is disabled
    [Arguments]  ${name}
    Wait until keyword succeeds  10s  0.5s  Element should be disabled  css=#contact-facetednav-action-${name}

Click the batch action
    [Arguments]  ${name}
    Click button  css=#contact-facetednav-action-${name}

The select all button shows
    [Arguments]  ${label}
    Wait until keyword succeeds  10s  0.5s  Element attribute value should be  ${SELECT_ALL}  value  ${label}

Click the select all button
    Click button  ${SELECT_ALL}

Accept the confirmation dialog
    [Documentation]  JavaScript confirm()
    Handle alert  ACCEPT

The batch actions message contains
    [Documentation]  status message shown above the batch actions once the results are refreshed
    [Arguments]  ${text}
    Wait until element contains  ${BATCH_ACTIONS}  ${text}

Click the contact action
    [Documentation]  per-contact action link (edit-contact, delete-contact)
    [Arguments]  ${name}  ${path}
    ${uid}=  Uid of  ${path}
    Wait until element is visible  css=#contact-action-${name}-${uid}
    Click element  css=#contact-action-${name}-${uid}

Click the create link
    [Documentation]  link of the "faceted-add" zone: organization, person or contact
    [Arguments]  ${type}
    Wait until element is visible  css=#faceted-add a.faceted-add-${type}
    Click link  css=#faceted-add a.faceted-add-${type}

Set the maximum number of contacts for select all
    [Documentation]  contactfacetednav.SELECT_ALL_MAX (set by the packages using the selection), then refresh the results
    [Arguments]  ${max}
    # contacts reset: "Select the contact" then waits for the contacts of the new results
    Execute javascript  contactfacetednav.SELECT_ALL_MAX = ${max}; contactfacetednav.contacts = undefined; Faceted.Form.do_form_query();

Record the posted forms
    [Documentation]  forms submitted by javascript are recorded (action and data), not sent
    Execute javascript  window.cfnPostedForms = []; HTMLFormElement.prototype.submit = function () { window.cfnPostedForms.push(this.action + ' ' + jQuery(this).serialize()); };

A form was posted to
    [Documentation]  action url and serialized data of a recorded form
    [Arguments]  ${url}  ${data}
    Wait for condition  return (window.cfnPostedForms || []).indexOf('${url} ${data}') !== -1

*** Settings ***
Documentation  Selection of contacts (javascript.js: contactfacetednav.contacts, select all, batch buttons).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open the faceted directory with the actions
Test Teardown  Close all browsers


*** Keywords ***
Open the faceted directory with the actions
    Open a manager browser
    Enable the contact actions
    Open the faceted directory


*** Test Cases ***
Selecting contacts updates the selected number and the batch buttons
    The selected contacts number is  0
    The batch action is disabled  delete
    The batch action is disabled  excelexport
    The select all button shows  Select all
    Select the contact  armeedeterre
    The selected contacts number is  1
    The batch action is enabled  delete
    The batch action is enabled  excelexport
    The select all button shows  Unselect all
    Select the contact  armeedeterre/corpsa
    The selected contacts number is  2
    Select the contact  armeedeterre
    Select the contact  armeedeterre/corpsa
    The selected contacts number is  0
    The batch action is disabled  delete

Select all then unselect all
    Select the contact  armeedeterre
    Click the select all button
    The selected contacts number is  0
    The select all button shows  Select all
    Click the select all button
    The selected contacts number is  7
    Checkbox should be selected  css=#faceted-results .contact-selection input
    The select all button shows  Unselect all
    Click the select all button
    The selected contacts number is  0
    Checkbox should not be selected  css=#faceted-results .contact-selection input

Select all is disabled when the results exceed the maximum
    # Plone 4 bug (MIGRATION.md, Known issues): the state is only computed when the selection changes,
    # not when the contacts are loaded, hence the selection of a contact
    Set the maximum number of contacts for select all  5
    Select the contact  armeedeterre
    Select the contact  armeedeterre
    Wait until keyword succeeds  10s  0.5s  Element should be disabled  ${SELECT_ALL}
    Element attribute value should be  ${SELECT_ALL}  title  Results is too large for mass selection (> 5)
    Show the contacts of type  person
    The results show  Rambo
    Wait until element is enabled  ${SELECT_ALL}

The selection is given to the other packages by the contactfacetednav javascript API
    # used by collective.contact.duplicated, collective.contact.contactlist, imio.dms.mail
    Select the contact  armeedeterre
    Select the contact  armeedeterre/corpsb
    ${uid1}=  Uid of  armeedeterre
    ${uid2}=  Uid of  armeedeterre/corpsb
    ${expected}=  Evaluate  ' '.join(sorted(['${uid1}', '${uid2}']))
    ${uids}=  Execute javascript  return contactfacetednav.contacts.selection_uids().sort().join(' ')
    Should be equal  ${uids}  ${expected}
    ${pathes}=  Execute javascript  return contactfacetednav.contacts.selection_pathes().sort().join(' ')
    Should be equal  ${pathes}  /${PLONE_SITE_ID}/mydirectory/armeedeterre /${PLONE_SITE_ID}/mydirectory/armeedeterre/corpsb
    ${data}=  Execute javascript  return contactfacetednav.serialize_uids(['a', 'b']) + ' ' + contactfacetednav.serialize_pathes(['/p'])
    Should be equal  ${data}  uids%3Alist=a&uids%3Alist=b pathes%3Alist=%2Fp

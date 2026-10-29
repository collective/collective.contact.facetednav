*** Settings ***
Documentation  "Create ..." links of the faceted-add zone (preview-items.pt), shown to the users who may add content.
...            The links carry the searched text for the add form, but Plone ignores form values sent by GET
...            (MIGRATION.md, Known issues): the scenarios don't check a prefilled value.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The create organization link adds an organization in a modal and refreshes the results
    Open the faceted directory
    Search the text  Navy
    The no result message is shown
    Click the create link  organization
    The modal is open
    ${title}=  Modal element  form-widgets-IBasic-title
    Input text  ${title}  Navy
    Save the modal
    The modal is closed
    The results show  Navy

The create person link opens the person add form
    Open the faceted directory
    Show the contacts of type  person
    The results show  Rambo
    Search the text  Jean Dupont
    The no result message is shown
    Click the create link  person
    Wait until page contains element  css=#form-widgets-lastname
    Location should contain  /mydirectory/++add++person

The create contact link opens the add contact form in a modal
    Open the faceted directory
    Show the contacts of type  held_position
    The results show  Sergent de la brigade LH
    Search the text  Jean Dupont
    The no result message is shown
    Click the create link  contact
    The modal is open
    ${form}=  Modal element  oform
    Page should contain element  ${form}

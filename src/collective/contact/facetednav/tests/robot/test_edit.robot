*** Settings ***
Documentation  Per-contact edit link: edit form in an overlay (Plone 4) / modal (Plone 6), results refreshed on save.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The edit link of a contact opens the edit form in a modal and saving refreshes the results
    Enable the contact actions
    Open the faceted directory
    Show the contacts of type  person
    The results show  Rambo
    Click the contact action  edit-contact  rambo
    The modal is open
    ${lastname}=  Modal element  form-widgets-lastname
    Input text  ${lastname}  Rimbaud
    Save the modal
    The modal is closed
    The results show  John Rimbaud
    The results do not show  Rambo

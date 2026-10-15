*** Settings ***
Documentation  Deletion of contacts: "Delete selected contacts" batch action (delete_selection)
...            and per-contact delete link (overlay / modal).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open the persons with the actions
Test Teardown  Close all browsers


*** Keywords ***
Open the persons with the actions
    Open a manager browser
    Enable the contact actions
    Open the faceted directory
    Show the contacts of type  person
    The results show  Rambo


*** Test Cases ***
Deleting the selected contacts removes them from the results
    Select the contact  rambo
    Select the contact  draper
    Click the batch action  delete
    Accept the confirmation dialog
    The batch actions message contains  2 object(s) deleted
    The results do not show  Rambo
    The results do not show  John Draper
    The results show  Pepper

The delete link of a contact deletes it after confirmation in a modal
    Click the contact action  delete-contact  rambo
    The modal is open
    Confirm the deletion in the modal
    The modal is closed
    The results do not show  Rambo
    The results show  Pepper

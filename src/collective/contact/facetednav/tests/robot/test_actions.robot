*** Settings ***
Documentation  "Enable actions" / "Disable actions" items of the Actions menu (subtyper, actions.xml).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
Enabling then disabling the contact actions from the Actions menu
    Open the faceted directory
    The contacts have no selection box
    Click the content action  faceted.actions.enable
    The status message contains  Contacts actions enabled
    The contacts have a selection box
    Click the content action  faceted.actions.disable
    The status message contains  Contacts actions disabled
    The contacts have no selection box

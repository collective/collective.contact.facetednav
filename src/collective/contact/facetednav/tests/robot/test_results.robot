*** Settings ***
Documentation  Results of the faceted directory (query.pt, preview-items.pt, preview-*.pt).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The faceted directory shows the contacts of the selected type
    Open the faceted directory
    The results show  Corps B
    The results do not show  Rambo
    Show the contacts of type  person
    The results show  Rambo
    The results show  Charles De Gaulle
    The results do not show  Corps B
    Show the contacts of type  held_position
    The results show  Sergent de la brigade LH

A search without result shows the no result message and the create link
    Open the faceted directory
    Search the text  Navy
    The no result message is shown
    Page should contain link  css=#faceted-add a.faceted-add-organization

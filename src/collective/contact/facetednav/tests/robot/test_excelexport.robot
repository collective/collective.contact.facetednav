*** Settings ***
Documentation  "Excel export" batch action (registered when collective.excelexport is installed, a dependency
...            of collective.documentgenerator): contactfacetednav.excel_export posts the selected uids to the
...            collective.excelexport search export. The answer is a file download (nothing to see in the page):
...            the scenario checks the form the browser posts.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  contactfacetednav.robot
Test Setup  Open a manager browser
Test Teardown  Close all browsers


*** Test Cases ***
The excel export action posts the selected contacts to the export view
    Enable the contact actions
    Open the faceted directory
    Select the contact  armeedeterre
    Record the posted forms
    Click the batch action  excelexport
    ${uid}=  Uid of  armeedeterre
    A form was posted to  ${PLONE_URL}/@@collective.excelexport?excelexport.policy=excelexport.search  UID%3Alist=${uid}

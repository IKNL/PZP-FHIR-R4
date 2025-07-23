This page specifies the technical process for how Advance Care Planning (ACP) information is exchanged between actors using the FHIR API. There are two primary methods for retrieving ACP information:

1. As a form. Fetching `QuestionnaireResponse` resource(s). This contains the patient's answers of an ACP questionnaire.
2. As individual resources. By fetching specific resources (`Consent`, `Goal`, `Observation`, etc.) that together form the patient's ACP.

### General Considerations

1. **Authorization**: Accessing ACP information is subject to strict privacy rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data.
2. **Patient Context**: All queries described in this guide are patient-specific. The client MUST know the logical ID of the patient in question and include it in every query (e.g., `patient=123` or `subject=Patient/123`). 
3. **Resolving references**: The returned resources may contain nested resources or references to other resources (like `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent requests to resolve these references and display the full details.

### Retrieve ACP QuestionnaireResponse

This approach is used to retrieve the complete, user-entered ACP document in its original context. It retrieves `QuestionnaireResponse` resources that contain the patient's answers.

##### Client Request

A client retrieves the QuestionnaireResponse by performing a GET search operation on the /QuestionnaireResponse endpoint. The search MUST be scoped to a specific patient and SHOULD filter by the canonical URL of the official ACP Questionnaire.

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://fhir.iknl.nl/fhir/ACP/Questionnaire/ACP-Form-R4

##### Server Response

Standard FHIR rules apply: 

* Success: `200 OK`. The server will return a Bundle containing the matching QuestionnaireResponse resource(s) for the patient.
* Not Found: If the patient has not completed an ACP questionnaire, the server will return a 200 OK with an empty Bundle.

### Retrieve ACP as Individual Resources

This approach is useful for applications that need to query specific parts of a patient's ACP, like treatment wishes or stated goals. While it requires multiple API calls, it provides more granular control.

##### Client Requests

| Information | Search URL|
|-|-|
|Treatment Directives | GET [base]/Consent?patient=[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope\|treatment&category=http://snomed.info/sct\|129125009|
|AdvanceDirectives|GET [base]/Consent?patient=[id]&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes\|acd|
|ACP Consultation and participants involed |GET [base]/Encounter?patient=[id]_include=Encounter:participant|
|ContactPersons | GET [base]/RelatedPerson?patient=[id]|
|Patient's Stated Goals|GET [base]/Goal?patient=[id]|
|Specific Wishes & Plans |GET [base]/Observation?patient=[id]&code=http://snomed.info/sct\|153851000146100,395091006,340171000146104,247751003
|Related Medical Devices (e.g., ICD)|GET [base]/DeviceUseStatement?patient=[id]&_has:Device:device:type:in=https://fhir.iknl.nl/fhir/ValueSet/ACP-MedicalDeviceProductType-ICD |


##### Server Response

Standard FHIR rules apply for every resource request: 

* Success: `200 OK`. The server will return a Bundle containing the matching resource(s) for the patient.
* Not Found: If the patient has no matching resources, the server will return a 200 OK with an empty Bundle.
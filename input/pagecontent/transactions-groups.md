This guide specifies how a client application can retrieve a patient's Advance Care Planning (ACP) documents and related clinical information from the FHIR server. There are two primary methods for retrieving this information:

1. As a single, comprehensive document: Using the QuestionnaireResponse resource, which contains all the patient's answers from an ACP questionnaire.
2. As individual, granular resources: By querying specific resources (Consent, Goal, Observation, etc.) that together form the patient's ACP.

### General Considerations
#### Authorization
Accessing ACP information is subject to strict privacy rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism, such as OAuth 2.0 with SMART on FHIR profiles, to obtain an access token with the necessary scopes to read the patient's clinical data.

#### Patient Context
All queries described in this guide are patient-specific. The client MUST know the logical ID of the patient in question and include it in every query (e.g., patient=123 or subject=Patient/123). 


### Method 1: Retrieve the ACP as a QuestionnaireResponse
This approach is used to retrieve the complete, user-entered ACP document in its original context. It retrieves `QuestionnaireResponse` resources that bundles the patient's answers.

#### Interaction
A client retrieves the QuestionnaireResponse by performing a GET search operation on the /QuestionnaireResponse endpoint. The search MUST be scoped to a specific patient and SHOULD filter by the canonical URL of the official ACP Questionnaire.

A search on the `/QuestionnaireResponse` end point

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://fhir.iknl.nl/fhir/ACP/Questionnaire/ACP-Form

#### Server Response
Success: `200 OK`. The server will return a Bundle containing the matching QuestionnaireResponse resource(s) for the patient.

Not Found: If the patient has not completed an ACP questionnaire, the server will return a 200 OK with an empty Bundle.

Note: The returned `QuestionnaireResponse` may contain nested resources or references to other resources (like `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent queries to resolve these references and display the full details.

### Method 2: Retrieve Individual ACP Resources

This approach is useful for applications that need to query specific components of a patient's ACP, such as only their treatment wishes or documented goals. This method requires multiple API calls, but offers more granular control.

#### Treatment Directives (e.g., limitations)

> GET [base]/Consent?patient=[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment
General Advance Directives
FHIR Resource:
Consent

> GET [base]/Consent?patient=[id]&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd

#### ACP Conversations (and who was involved)


> GET [base]/Encounter?patient=[id]_include=Encounter:participant


#### Patient's Stated Goals

> GET [base]/Goal?patient=[id]

#### Specific Wishes & Plans (as observations)

> GET [base]/Observation?patient=[id]&code=153851000146100,395091006,340171000146104,247751003
Codes for: patient wishes, end of life plan, treatment wishes, resuscitation wishes

#### Related Medical Devices (e.g., ICD)

> GET [base]/DeviceUseStatement?patient=[id]
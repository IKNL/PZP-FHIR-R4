This guide specifies how to exchange Advance Care Planning (ACP) data using FHIR. It is divided into two sections:

* An overview and guidance of the FHIR resources used to represent the ACP dataset, many of which are based on ZIB profiles.
* The technical process for exchanging the ACP dataset between a client and a server.

### Representing ACP Data in FHIR

#### The ACP Questionnaire
A patient's ACP preferences can be captured using a structured form, such as the one developed by IKNL. This implementation guide provides a corresponding FHIR Questionnaire resource to ensure standardized data collection. [ADD link and improve] 


#### FHIR Data Model
The diagram below shows the FHIR data model, organized into three categories for clarity: ACP Consultation, ACP Agreements, and Supporting Information.

* ACP Consultation: Captures the event where ACP is discussed, whether through a conversation or by completing the questionnaire.
* ACP Agreements: Documents the patient's specific wishes. When gathered from a conversation, resources like Observation are used. When gathered from the form, the data is stored in a QuestionnaireResponse resource.
* Supporting Information: Contains contextual information about the individuals involved

{% include fhir-data-model-mermaid-diagram.md %}


#### Associating dataset to FHIR - Mapping overview
The FHIR profiles in this guide have a traceable mapping to their ART-DECOR dataset counterparts.
The version of the ART-DECOR dataset used is registered in the `StructureDefinition.mapping.identity` element. The mapping for each individual data element is defined in its `ElementDefinition.mapping`. A user-friendly rendering of these mappings is available on the "Mappings" tab of each profile page.


{% include mappings.md %}


### Exchanging ACP information
The following sections specify how ACP information is exchanged between actors. Here are some **general considerations**.

#### Authorization
Accessing ACP information is subject to strict privacy rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data.

#### Patient Context
All queries described in this guide are patient-specific. The client MUST know the logical ID of the patient in question and include it in every query (e.g., `patient=123` or `subject=Patient/123`). 

#### Resolving references
The returned resources may contain nested resources or references to other resources (like `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent requests to resolve these references and display the full details.

### Retrieving ACP Information
There are two primary methods for retrieving ACP information:

1. As a form. Fetching QuestionnaireResponse resource(s). This contains the patient's answers of an ACP questionnaire.
2. As individual resources. By fetching specific resources (Consent, Goal, Observation, etc.) that together form the patient's ACP.

#### Retrieve as a QuestionnaireResponse
This approach is used to retrieve the complete, user-entered ACP document in its original context. It retrieves `QuestionnaireResponse` resources that contain the patient's answers.

##### Client Request
A client retrieves the QuestionnaireResponse by performing a GET search operation on the /QuestionnaireResponse endpoint. The search MUST be scoped to a specific patient and SHOULD filter by the canonical URL of the official ACP Questionnaire.

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://fhir.iknl.nl/fhir/ACP/Questionnaire/ACP-Form-R4

##### Server Response
Default FHIR rules apply: 

* Success: `200 OK`. The server will return a Bundle containing the matching QuestionnaireResponse resource(s) for the patient.
* Not Found: If the patient has not completed an ACP questionnaire, the server will return a 200 OK with an empty Bundle.

#### Retrieve Individual ACP Resources
This approach is useful for applications that need to query specific parts of a patient's ACP, like treatment wishes or stated goals. While it requires multiple API calls, it provides more granular control.


| Information | Search URL|
|-|-|
|Treatment Directives (e.g., limitations)| GET [base]/Consent?patient=[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope\|treatment|
|AdvanceDirectives|GET [base]/Consent?patient=[id]&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes\|acd|
|ACP Conversations (and who was involved)|GET [base]/Encounter?patient=[id]_include=Encounter:participant|
|Patient's Stated Goals|GET [base]/Goal?patient=[id]|
| Specific Wishes & Plans (as observations)
Codes for: patient wishes, end of life plan, treatment wishes, resuscitation wishes |GET [base]/Observation?patient=[id]&code=http://snomed.info/sct\|153851000146100,395091006,340171000146104,247751003
|Related Medical Devices (e.g., ICD)|GET [base]/DeviceUseStatement?patient=[id]|
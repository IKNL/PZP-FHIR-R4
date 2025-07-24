This page describes the two primary methods for retrieving a patient's Advance Care Planning (ACP) information using the FHIR API. The best method depends on your application's needs.

1. As a form. Fetching `QuestionnaireResponse` resource(s). This contains the patient's answers of an ACP questionnaire.
2. As individual resources. By fetching specific resources (`Consent`, `Goal`, `Observation`, etc.) that together form the patient's ACP. See <a href="data-model.html">Data Model page</a> for a complete overview.

---

### General API requirements

All interactions adhere to the following principles.

1. **Authorization**: Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts.
2. **Patient Context**: All queries described in this guide are patient-specific. The client MUST know the logical ID of the patient in question and include it in every query (e.g., `patient=123` or `subject=Patient/123`). This may require an initial request on the Patient endpoint with a search using a patient identifier like the BSN. This may also be described by other technical agreements.
3. **Resolving references**: The returned resources may contain nested resources or references to other resources (like `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent requests to resolve these references and display the full details.

---

### Method 1: Retrieve ACP QuestionnaireResponse

This approach is used to retrieve the complete, user-entered ACP document in its original context. It retrieves `QuestionnaireResponse` resources that contain the patient's answers.

#### Client Request

A client retrieves the `QuestionnaireResponse` by performing a `GET` search operation. The search is scoped to a specific patient and is filtered by the canonical URL of the official ACP questionnaire to ensure that only the correct form is returned.

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://fhir.iknl.nl/fhir/ACP/Questionnaire/ACP-Form-R4


#### Server Response

The server follows standard FHIR response rules:

* Success: 200 OK. The response body will contain a Bundle with the matching QuestionnaireResponse resource(s).
* Not Found: 200 OK. If the patient has not completed the questionnaire, the server will return an empty Bundle.

##### Server Response

Standard FHIR rules apply: 

* Success: `200 OK`. The server will return a Bundle containing the matching QuestionnaireResponse resource(s) for the patient.
* Not Found: If the patient has not completed an ACP questionnaire, the server will return a 200 OK with an empty Bundle.

---

### Method 2: Retrieve ACP as Individual Resources

This approach provides granular access to the individual clinical statements that constitute the ACP. It allows applications to query for specific data points without processing an entire form.

This approach is useful for applications that need to query specific parts of a patient's ACP, like treatment wishes or stated goals. While it requires multiple API calls, it provides more granular control and returns the ACP in usable resources. The below client requests are in scope of a Patient's context for which an initial request may be needed to match the Patient resource id with a identifier (e.g. BSN)

#### Client Requests

The below listed search request show how all the relevant ACP **Consultation**,  **Agreements** and **Supporting Information** can be retrieved. Information on all **Individuals** are referenced from these resources and be retrieved using the `_include` statement as defined below, or by resolving the references. Standard FHIR rules apply on the search syntax.

```
Consultation

1 GET [base]/Procedure?patient=[id]&code=http://snomed.info/sct|713603004&_include:Procedure:encounter

Agreements

2 GET [base]/Consent?patient=[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment&category=http://snomed.info/sct|129125009&_include=Consent:actor

3 GET [base]/Consent?patient=[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope|adr&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd&_include=Consent:actor

4 GET [base]/Goal?patient=[id]&category=http://snomed.info/sct|713603004

5 GET [base]/Observation?patient=[id]&code=http://snomed.info/sct|153851000146100,395091006,340171000146104,247751003

Supporting information

6 GET [base]/DeviceUseStatement?patient=[id]&device.type:in=https://fhir.iknl.nl/fhir/ValueSet/ACP-MedicalDeviceProductType-ICD&_include:DeviceUseSatement:device

7 GET [base]/Communication?patient=[id]&reason-code=http://snomed.info/sct|713603004
```

1. Retrieves `Procedure` resources that are advance care planning procedures and include the `Encounter` resource in which the advance care planning procedure took place.
2. Retrieves `Consent` resources that are TreatmentDirectives and include the agreement parties (Patient and/or ContactPersons and HealthProfessionals).
3. Retrieves `Consent` resources AdvanceDirectives and include the representatives (ContactPersons).
4. Retrieves `Goal` resources that relate to advance care planning.
5. Retrieves `Observation` resources that are about specific wishes and plans as defined by profiles defined in the IG.
6. Retrieves `DeviceUseStatement` resources that have a `Device` that represent an ICD and include the `Device`.
7. Retrieves `Communicaton` resources that represent all communication events related to the advance care planning procedure.

#### Advanced Search Parameters to be supported
Custom search parameters:
* The `reason-code` parameter to search on `Communication.reasonCode`. See the custom `SearchParemeter` resource definition in the artifacts tab.

The queries above utilize several search parameters types and modifiers:

* `_include`: Used to also return the referenced resources in the same `Bundle`, reducing the need for subsequent API calls.
* `in`: A modifier that allows searching against a ValueSet. In this client requests mentioned above, it checks if the device's type is in the specified ValueSet of ICD products.

#### Server Response

Standard FHIR rules apply for every resource request: 

* Success: `200 OK`. The server will return a Bundle containing the matching resource(s) for the patient.
* Not Found: If the patient has no matching resources, the server will return a 200 OK with an empty Bundle.
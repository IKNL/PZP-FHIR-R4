This page describes the two primary methods for retrieving a patient's Advance Care Planning (ACP) information using the FHIR API. The best method depends on your application's needs.
1. As individual resources. By fetching specific resources (`Consent`, `Goal`, `Observation`, etc.) that together form the patient's ACP. See <a href="data-model.html">Data Model page</a> for a complete overview.
2. As a form. Fetching `QuestionnaireResponse` resource(s). This contains the ACP agreements recorded according to the structured form for uniform registration of ACP.

---

### General API requirements

All interactions adhere to the following principles.

1. **Authorization**: Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data. The exact methods may be found in the used infrastructure specification and agreements of e.g. LSP, Twiin and or Nuts.
2. **Patient Context**: All queries described in this guide are patient-specific. The client MUST know the logical ID of the patient in question and include it in every query (e.g., `patient=123` or `subject=Patient/123`). This may require an initial request on the Patient endpoint with a search using a patient identifier like the BSN. This may also be described by other technical agreements.
3. **Resolving references**: The returned resources may contain nested resources or references to other resources (like `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent requests to resolve these references and display the full details.

---

### Method 1: Retrieve ACP as Individual Resources

This approach provides granular access to the individual clinical statements that constitute the ACP. It allows applications to query for specific data points without processing an entire form.

This approach is useful for applications that need to query specific parts of a patient's ACP, like treatment wishes or stated goals. While it requires multiple API calls, it provides more granular control and returns the ACP in usable resources. The below client requests are in scope of a Patient's context for which an initial request may be needed to match the Patient resource id with a identifier (e.g. BSN).

#### Client Requests

The below listed search request show how all the ACP agreements, procedural information and relevant clinical context can be retrieved. Information on individuals involved in the ACP process are referenced from these resources and can be retrieved using the `_include` statement as defined below, or by resolving the references. Standard FHIR rules apply on the search syntax.

```
1a GET [base]/Procedure?patient=[id]&code=http://snomed.info/sct|713603004&_include:Procedure:encounter

1b GET [base]/Encounter?patient=[id]&reason=http://snomed.info/sct|713603004

2 GET [base]/Consent?patient=[id]&category=http://snomed.info/sct|11291000146105&_include=Consent:actor

3 GET [base]/Consent?patient=[id]&category=http://snomed.info/sct|11341000146107&_include=Consent:actor

4 GET [base]/Goal?patient=[id]&description:in=https://fhir.iknl.nl/fhir/ValueSet/ACP-MedicalPolicyGoal

5 GET [base]/Observation?patient=[id]&code=http://snomed.info/sct|153851000146100,395091006,340171000146104,247751003

6 GET [base]/DeviceUseStatement?patient=[id]&device.type:in=https://fhir.iknl.nl/fhir/ValueSet/ACP-MedicalDeviceProductType-ICD&_include:DeviceUseSatement:device

7 GET [base]/Communication?patient=[id]&reason-code=http://snomed.info/sct|713603004
```

1. Both requests are designed to retrieve the same information, but with different approaches:
    * A) Retrieves `Procedure` resources representing ACP procedures and includes the associated `Encounter` resource where the procedure took place.
    * B) Retrieves `Encounter` resources that list an ACP procedure as their reason. Request A is generally preferred because `Encounter.patient` may not always be present; if absent, it indicates the patient was not involved in the Encounter. Using request A ensures these cases are included as well.
2. Retrieves `Consent` resources for Treatment Directives and includes the agreement parties (Patient, ContactPersons, and HealthProfessionals).
3. Retrieves `Consent` resources for Advance Directives and includes the representatives (ContactPersons).
4. Retrieves `Goal` resources with a Medical Policy Goal code in the `Goal.description`.
5. Retrieves `Observation` resources related to specific wishes and plans, as defined by the profiles in the Implementation Guide.
6. Retrieves `DeviceUseStatement` resources for devices representing an ICD, and includes the corresponding `Device` resource.
7. Retrieves `Communication` resources representing all communication events related to the ACP procedure.

#### Advanced Search Parameters Supported

Custom search parameters:
* The `reason-code` parameter allows searching on `Communication.reasonCode`. See the custom `SearchParameter` resource definition in the artifacts tab.
* The `description` parameter allows searching on `Goal.description`. This search parameter is defined from R5 onwards. The parameter definition can be found in the <a href="https://hl7.org/fhir/searchparameter-registry.html#:~:text=Goal.%E2%80%8Bcategory-,description,-token">Search Parameter Registry</a> and be applied for this version.

The queries above use several search parameter types and modifiers:
* `_include`: Returns referenced resources in the same `Bundle`, reducing the need for additional API calls.
* `in`: A modifier that enables searching against a ValueSet. In the client requests above, it checks if the device type is included in the specified ValueSet of ICD products.
* Chained parameters: Used for searching within referenced resources. For example, to find `DeviceUseStatement` resources with a specific `Device`, or `Encounter` resources that have an advance care planning `Procedure` as their reason.

#### Server Response

Standard FHIR rules apply for every resource request: 

* Success: `200 OK`. The server will return a Bundle containing the matching resource(s) for the patient.
* Not Found: If the patient has no matching resources, the server will return a 200 OK with an empty Bundle.

---

### Method 2: Retrieve ACP QuestionnaireResponse

This approach is used to retrieve the complete form for uniform registration of ACP in its original context. It retrieves `QuestionnaireResponse` resources that contain the content discussed by the individuals involved in the ACP conversation.

#### Client Request

A client retrieves the `QuestionnaireResponse` by performing a `GET` search operation. The search is scoped to a specific patient and is filtered by the canonical URL of the <a href="Questionnaire-ACP-zib2017.html">ACP Questionnaire</a> to ensure that only the correct form is returned.

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://fhir.iknl.nl/fhir/Questionnaire/ACP-zib2017


#### Server Response

The server follows standard FHIR response rules:

* Success: `200 OK`. The response body will contain a Bundle with the matching QuestionnaireResponse resource(s). Example QuestionnaireResponse resources are available <a href="QuestionnaireResponse-HendrikHartman-20201001.html">here</a> and <a href="QuestionnaireResponse-HendrikHartman-20221108.html">here</a>.
* Not Found: `200 OK`. If there is no completed form for this patient, the server will return an empty Bundle.
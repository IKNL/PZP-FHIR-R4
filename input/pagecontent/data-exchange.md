This page describes the two transaction methods for exchanging a patient's Advance Care Planning (ACP) information using RESTful API.

1. <a href="#method-1-retrieve-acp-as-individual-resources">As individual resources.</a> By fetching specific resources (`Consent`, `Goal`, `Observation`, etc.) that together form the patient's ACP. See <a href="data-model.html">Data Model page</a> for a complete overview.
2. <a href="#method-2-retrieve-acp-questionnaireresponse">As a form.</a> Fetching `QuestionnaireResponse` resource(s). This contains the ACP agreements recorded according to the structured form for uniform registration of ACP.

### Conformance Requirements Actors

This implementation guide defines two actors, each with their own CapabilityStatements that specify the capabilities required for compliance:
- <a href="ActorDefinition-ACPActorConsulter.html">ACP Actor Consulter</a>: A client application that retrieves a patient's ACP information following this <a href="CapabilityStatement-ACP-CapabilityStatementConsulter.html">CapabilityStatement</a>.
- <a href="ActorDefinition-ACPActorProvider.html">ACP Actor Provider</a>: A server application that exposes a patient's ACP information following this <a href="CapabilityStatement-ACP-CapabilityStatementProvider.html">CapabilityStatement</a>.

To be conformant the ACP Actor Consulter SHALL support both transaction groups. This ensures the actor can retrieve ACP information from any provider, regardless of the exchange method implemented.
The ACP Actor Provider SHALL support at least one of the two transaction groups. The individual resources method is preferred over the form-based method for system-to-system exchange, as it offers a more standardized and reusable data structure.


### General API requirements

This IG focuses solely on defining how ACP health information is accessed and structured for data exchange. It does not specify supporting functionalities such as addressing, routing, localization, consent management, or authentication. These capabilities are expected to be provided by the underlying infrastructure specifications and agreements in use, such as Generic Functions, LSP, Twiin, or Nuts.

Within this scope, the following requirements apply:

1. **Authorization**: Accessing ACP information is subject to strict privacy and security rules. All API requests MUST be properly authenticated and authorized. The client application is expected to use a secure mechanism to obtain an access token with the necessary scopes to read the patient's clinical data.
2. **Patient Context**: All queries described in this guide are patient-specific. The client needs to know the logical ID of the patient and include it in every query (e.g., `patient=123` or `subject=Patient/123`). The method for obtaining the patient's logical ID is not specified in this IG, but may include: an initial search request on the Patient endpoint using a patient identifier such as the BSN; interactions as defined in [IHE PDQm ITI-119](https://profiles.ihe.net/ITI/PDQm/3.2.0/ITI-119.html); or any other method provided by the infrastructure.
3. **Resolving References**: The returned resources may contain nested resources or references to other resources (such as `Practitioner` or `RelatedPerson`). The client application may need to perform subsequent requests to resolve these references and display the full details.

---

### Method 1: Retrieve ACP as Individual Resources

This approach provides granular access to the individual clinical statements that constitute the ACP. It allows applications to query for specific data points without processing an entire form.

This approach is useful for applications that need to query specific parts of a patient's ACP, like treatment wishes or stated goals. While it requires multiple API calls, it provides more granular control and returns the ACP in usable resources. The below listed client requests are in scope of a Patient's context for which an initial request may be needed to match the Patient resource id with an identifier (e.g. BSN).

#### Client Requests

The below listed search requests show how all the ACP agreements, procedural information and relevant clinical context can be retrieved. Information on individuals involved in the ACP process are referenced from these resources and can be retrieved using the `_include` statement as defined below, or by resolving the references. Standard FHIR rules apply on the search syntax. The <a href="CapabilityStatement-ACP-CapabilityStatementProvider.html">Provider CapabilityStatement</a> and <a href="CapabilityStatement-ACP-CapabilityStatementConsulter.html">Consulter CapabilityStatement</a> resources may provide a more structured overview of the below requirements.

```
1a GET [base]/Procedure?patient=Patient/[id]&code=http://snomed.info/sct|713603004,urn:oid:2.16.840.1.113883.2.4.3.120.5.3|411600B,urn:oid:2.16.840.1.113883.2.4.3.27.15.5|190099&_include=Procedure:encounter

1b GET [base]/Encounter?patient=Patient/[id]&reason-reference:Procedure.code=http://snomed.info/sct|713603004,urn:oid:2.16.840.1.113883.2.4.3.120.5.3|411600B,urn:oid:2.16.840.1.113883.2.4.3.27.15.5|190099&_include=Encounter:reason-reference

2 GET [base]/Consent?patient=Patient/[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope|treatment&category=http://snomed.info/sct|129125009&_include=Consent:actor

3 GET [base]/Consent?patient=Patient/[id]&scope=http://terminology.hl7.org/CodeSystem/consentscope|adr&category=http://terminology.hl7.org/CodeSystem/consentcategorycodes|acd&_include=Consent:actor

4 GET [base]/Goal?patient=Patient/[id]&category=http://snomed.info/sct|713603004

5 GET [base]/Observation?patient=Patient/[id]&code=http://snomed.info/sct|665671000146101,http://snomed.info/sct|153851000146100,http://snomed.info/sct|395091006,http://snomed.info/sct|340171000146104,http://snomed.info/sct|247751003,http://snomed.info/sct|570801000146104

6 GET [base]/DeviceUseStatement?patient=Patient/[id]&device.type=http://snomed.info/sct|72506001,http://snomed.info/sct|465460004,http://snomed.info/sct|468542000,http://snomed.info/sct|704707009,http://snomed.info/sct|1263462004,http://snomed.info/sct|1236894001&_include=DeviceUseStatement:device

7 GET [base]/CommunicationRequest?patient=[id]&category=http://snomed.info/sct|223449006
```

1. Both requests are designed to retrieve the same information, but with different approaches:
    * A) Retrieves `Procedure` resources representing ACP procedures and includes the associated `Encounter` resource where the procedure took place.
    * B) Retrieves `Encounter` resources that list an ACP procedure as their reason, and includes the referenced resources in the result. Request A is generally preferred because `Encounter.patient` may not always be present; if absent, it indicates the patient was not involved in the Encounter. Using request A ensures these cases are included as well.
2. Retrieves `Consent` resources for Treatment Directives and includes the agreement parties (Patient, ContactPersons, and HealthProfessionals).
3. Retrieves `Consent` resources for Advance Directives and includes the representatives (ContactPersons).
4. Retrieves `Goal` resources related to advance care planning.
5. Retrieves `Observation` resources related to specific wishes, plans and whether the patient is legally capable regarding medical treatment decisions, as defined by the profiles in the Implementation Guide.
6. Retrieves `DeviceUseStatement` resources for devices representing an ICD, and includes the corresponding `Device` resource.
7. Retrieves `CommunicationRequest` resources representing all communication requests related to the ACP procedure.

For `RelatedPerson` and `Practitioner` there is no specific query as according to the model there are references made to these resources. If there is a legal representative we expect that to be present in `Patient.contact`. For related persons attending the encounter a reference is expected to be made in `Encounter.participant`.

#### Advanced Search Parameters Supported
The queries above use several search parameter types and modifiers:
* `_include`: Returns referenced resources in the same `Bundle`, reducing the need for additional API calls.
* Chained parameters: Used for searching within referenced resources. For example, to find `DeviceUseStatement` resources with a specific `Device`, or `Encounter` resources that have an advance care planning `Procedure` as their reason.

#### Server Response

Standard FHIR rules apply for every resource request: 

* Success: `200 OK`. The server will return a Bundle containing the matching resource(s) for the patient.
* Not Found: If the patient has no matching resources, the server will return a 200 OK with an empty Bundle.

#### Sequence Diagram 

{% include fhir-data-exchange-individual-resources-mermaid-diagram.md %}

---

### Method 2: Retrieve ACP QuestionnaireResponse

This approach is used to retrieve the complete form for uniform registration of ACP in its original context. It retrieves `QuestionnaireResponse` resources that contain the content discussed by the individuals involved in the ACP conversation.

This method is included to lower the implementation burden for data providers who already use a form-based registration process. By allowing them to expose their existing form as a `QuestionnaireResponse`, it accelerates the availability of exchangeable ACP data. The trade-off is that this approach requires more effort from the ACP Actor Consulter, as they need to support multiple methods. The preferred method for system-to-system exchange is the individual resources method, as it offers a more standardized and reusable data structure.

#### Client Request

A client retrieves the `QuestionnaireResponse` by performing a `GET` search operation. The search is scoped to a specific patient and is filtered by the canonical URL of the <a href="Questionnaire-ACP-zib2020.html">ACP Questionnaire</a> to ensure that only the correct form is returned.

> GET [base]/QuestionnaireResponse?subject=Patient/[id]&questionnaire=https://api.iknl.nl/docs/pzp/r4/Questionnaire/ACP-zib2020


#### Server Response

The server follows standard FHIR response rules:

* Success: `200 OK`. The response body will contain a Bundle with the matching QuestionnaireResponse resource(s). Example QuestionnaireResponse resources are available <a href="QuestionnaireResponse-HendrikHartman-20201001.html">here</a> and <a href="QuestionnaireResponse-HendrikHartman-20221108.html">here</a>.
* Not Found: `200 OK`. If there is no completed form for this patient, the server will return an empty Bundle.

#### Sequence Diagram 

{% include fhir-data-exchange-questionnaireresponse-mermaid-diagram.md %}

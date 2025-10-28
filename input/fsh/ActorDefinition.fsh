Instance: ACPActorConsulter
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorConsulter"
* title = "ACP Actor Consulter"
* status = #active
* description = "The ACP Actor Consulter is a system that creates and initiates a data access request to retrieve digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL "Netherlands"
* type = #system
* documentation = "The ACP Actor Consulter is a system role fulfilled by a consulting information system (e.g., GP Information System (HIS), Electronic Patient Record (EPD), Electronic Client Record (ECD)). It is responsible for initiating the transaction to retrieve Advance Care Planning (ACP) information.

In the Dutch functional design, this role is identified as **PZPInformatieRaadplegendSysteem** with the code **PZP-PZPIR-FHIR**. This code is a composite of the use case (`PZP` - Proactieve Zorgplanning), the system role (`PZPIR` - PZP Informatie Raadplegend) and the standard for information exchange (`FHIR`).

An ACP Actor Consulter:

- **SHALL** accept resources containing obligation-marked elements without error\n\n 
- **SHALL** accept resources containing obligation-marked elements with missing data (e.g., usage of data-absent-reason extension) without error.\n\n

How the system processes the resource depends on local requirements that could align with obligation terms such as [reject invalid](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-reject-invalid), 
[correctly handle](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-handle), 
[persist](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-persist), 
[display](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-display), 
or [ignore](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-ignore).

\n\n The obligation-marked elements are specified in the ACP Actor Consulter [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

Instance: ACPActorProvider
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorProvider"
* title = "ACP Actor Provider"
* status = #active
* description = "The ACP Actor Provider is a system that responds to data access requests for digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL "Netherlands"
* type = #system
* documentation = "The ACP Actor Provider is a system role fulfilled by a source information system (e.g., GP Information System (HIS), Electronic Patient Record (EPD), Electronic Client Record (ECD)). It is responsible for making the Advance Care Planning (ACP) information available in response to a request.

In the Dutch functional design, this role is identified as **PZPInformatieBeschikbaarstellendSysteem** with the code **PZP-PZPIB-FHIR**. This code is a composite of the use case (`PZP` - Proactieve Zorgplanning), the system role (`PZPIB` - PZP Informatie Beschikbaarstellend) and the standard for information exchange (`FHIR`).

An ACP Actor Provider:

- **SHALL** correctly populate all obligation-marked elements if they know a value for the element.\n\n
- **SHALL** populate the data-absent-reason extension when an element cannot be shared due to policy or technical constraints.\n\n

The obligation-marked elements are specified in ACP Actor Provider [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

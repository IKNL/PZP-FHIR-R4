Instance: ACPActorRequester
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorRequester"
* title = "ACP Actor Requester"
* status = #active
* description = "The ACP Actor Requester is a system that creates and initiates a data access request to retrieve digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL "Netherlands"
* type = #system
* documentation = "The ACP Actor Requester is a system role fulfilled by a consulting information system (e.g., GP Information System (HIS), Electronic Patient Record (EPD), Electronic Client Record (ECD)). It is responsible for initiating the transaction to retrieve Advance Care Planning (ACP) information.

In the Dutch functional design, this role is identified as **PZPInformatieRaadplegendSysteem** with the code **PZP-RPZPI-PZPIR**. This code is a composite of the use case (`PZP` - Proactieve Zorgplanning), the transaction (`RPZPI` - Raadplegen PZP Informatie), and the system role (`PZPIR` - PZP Informatie Raadplegend).

An ACP Actor Requester:

- **SHALL** accept resources containing obligation-marked elements without error\n\n 
- **SHALL** accept resources containing obligation-marked elements with missing data (e.g., usage of data-absent-reason extension) without error.\n\n

How the system processes the resource depends on local requirements that could align with obligation terms such as [reject invalid](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-reject-invalid), 
[correctly handle](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-handle), 
[persist](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-persist), 
[display](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-display), 
or [ignore](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-ignore).

\n\n The obligation-marked elements are specified in the ACP Actor Requester [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

Instance: ACPActorResponder
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorResponder"
* title = "ACP Actor Responder"
* status = #active
* description = "The ACP Actor Responder is a system that responds to data access requests for digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL "Netherlands"
* type = #system
* documentation = "The ACP Actor Responder is a system role fulfilled by a source information system (e.g., GP Information System (HIS), Electronic Patient Record (EPD), Electronic Client Record (ECD)). It is responsible for making the Advance Care Planning (ACP) information available in response to a request.

In the Dutch functional design, this role is identified as **PZPInformatieBeschikbaarstellendSysteem** with the code **PZP-RPZPI-PZPIB**. This code is a composite of the use case (`PZP` - Proactieve Zorgplanning), the transaction (`RPZPI` - Raadplegen PZP Informatie), and the system role (`PZPIB` - PZP Informatie Beschikbaarstellend).

An ACP Actor Responder:

- **SHALL** correctly populate all obligation-marked elements if they know a value for the element.\n\n
- **SHALL** populate the data-absent-reason extension when an element cannot be shared due to policy or technical constraints.\n\n

The obligation-marked elements are specified in ACP Actor Responder [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

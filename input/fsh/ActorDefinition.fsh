Instance: ACPActorRequester
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorRequester"
* title = "ACP Actor Requester"
* status = #active
* description = "The ACP Actor Requester is a system that creates and initiates a data access request to retrieve digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL
* type = #system
* documentation = "An ACP Actor Client, also known as ACP Actor Requester:\n\n 
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
* jurisdiction = urn:iso:std:iso:3166#NL
* type = #system
* documentation = "An ACP Actor Server, also known as ACP Actor Responder:\n\n
- **SHALL** correctly populate all obligation-marked elements if they know a value for the element.\n\n
- **SHALL** populate the data-absent-reason extension when an element cannot be shared due to policy or technical constraints.\n\n

The obligation-marked elements are specified in ACP Actor Responder [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

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
- **SHALL** accept resources containing any valid value for *Must Support* elements without error\n\n 
- **SHALL** accept resources containing *Must Support* elements with [Missing Data](general-requirements.html#missing-data) 
or [Suppressed Data](general-requirements.html#suppressed-data) without error\n\n 

How the system processes the resource depends on local requirements that could align with obligation terms such as [reject invalid](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-reject-invalid), 
[correctly handle](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-handle), 
[persist](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-persist), 
[display](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-display), 
or [ignore](https://hl7.org/fhir/extensions/CodeSystem-obligation.html#obligation-ignore).

\n\n When a *Must Support* element requires additional or stronger obligation, this obligation is specified in the ACP Actor Requester [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

Instance: ACPActorResponder
InstanceOf: ActorDefinition
Usage: #example
* name = "ACPActorResponder"
* title = "ACP Actor Responder"
* status = #active
* description = "The ACP Actor Responder is a system that responds to data access requests for digital health and administrative information."
* jurisdiction = urn:iso:std:iso:3166#NL
* type = #system
* documentation = "An ACP Responder, also known as ACP Server:\n\n
- **SHALL** correctly populate all *Must Support* elements if they know a value for the element.\n\n
- **SHALL** implement the requirements on [Suppressed Data](general-requirements.html#suppressed-data) when an element is NOT allowed to be shared\n\n
- **SHALL** implement the requirements on [Missing Data](general-requirements.html#missing-data) when an element value is NOT known\n\n
When a *Must Support* element requires additional or stronger obligation, this obligation is specified in the AU Core Responder [obligation extension](https://hl7.org/fhir/extensions/StructureDefinition-obligation.html) on the element definition."

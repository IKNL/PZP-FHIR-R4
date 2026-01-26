Profile: ACPInformRelativesRequest
Parent: CommunicationRequest
Id: ACP-InformRelativesRequest
Title: "ACP Request to Inform Relatives"
Description: "A CommunicationRequest representing the advice or instruction given to the patient to discuss their advance care planning (ACP) and treatment agreements with their relatives or proxies."
* insert MetaRules
* category 1..*
* category = $snomed#223449006
* category ^comment = "The `category.text` element may be used to provide additional context for human readers next to the pattern category coding, for example: 'Request for patient to inform relatives about treatment agreements'."
* subject only Reference(ACPPatient)
* encounter only Reference(ACPEncounter)
* requester only Reference(ACPHealthProfessionalPractitionerRole or ACPHealthProfessionalPractitioner) 
* sender only Reference(ACPPatient)
* recipient only Reference(ACPContactPerson)
* reasonCode 1..*
* reasonCode = $snomed#713603004 // "advance care planning"

* insert ObligationRules(category) // already 1..1 so may not be needed place under obligation but added for consistency
* insert ObligationRules(subject)
* insert ObligationRules(encounter)
* insert ObligationRules(authoredOn) // not explicitly required/defined in dataset but important for context
* insert ObligationRules(requester)
* insert ObligationRules(sender)
* insert ObligationRules(recipient)
* insert ObligationRules(reasonCode) // already 1..1 so may not be needed place under obligation but added for consistency


Mapping: MapACPInformRelativesRequest
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPInformRelativesRequest
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "734" "Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken?"


Instance: ACP-InformRelativesRequest-Example1
InstanceOf: ACPInformRelativesRequest
Title: "ACP Request to Inform Relatives - Example 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "4dbg052d-570a-40e6-b3a8-0c48347747f2"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #active // either 'active' or 'completed' depending on whether the communication has taken place yet
* subject = Reference(ACP-Patient-HendrikHartman-Example1) "Patient, Hendrik Hartman"
* authoredOn = "2020-10-01"
* encounter = Reference(ACP-Encounter-Example1) "Encounter on 01-10-2020"
* requester = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Example1) "Healthcare professional (role), van Huissen"
* sender = Reference(ACP-Patient-HendrikHartman-Example1) "Patient, Hendrik Hartman"
//* recipient = "RelatedPerson xyz or family" // if there are known related persons they can be referenced here otherwise left out completely
* reasonCode = $snomed#713603004 "advance care planning"
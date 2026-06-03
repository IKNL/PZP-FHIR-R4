Profile: ACPInformRelativesRequest
Parent: CommunicationRequest
Id: ACP-InformRelativesRequest
Title: "ACP Request to Inform Relatives"
Description: "A CommunicationRequest representing the advice or instruction given to the patient to discuss their advance care planning (ACP) and treatment agreements with their relatives or proxies."
* insert MetaRules
* category 1..*
* category = $snomed#223449006
* category ^comment = "The `category.text` element may be used to provide additional context for human readers next to the pattern category coding, for example: 'Request for patient to inform relatives about treatment agreements'."
* subject 1..1
* subject only Reference(ACPPatient)
* encounter only Reference(ACPEncounter)
* requester 1..1
* requester only Reference(ACPHealthProfessionalPractitionerRole or ACPHealthProfessionalPractitioner) 
* sender 1..1
* sender only Reference(ACPPatient)
* recipient only Reference(ACPContactPerson)
* reasonCode 1..*
* reasonCode = $snomed#713603004 // "advance care planning"
* obeys cr-date-required

* insert ObligationRules(category) // already 1..1 so may not be needed place under obligation but added for consistency
* insert ObligationRules(subject)
* insert ObligationRules(encounter)
* insert ObligationRules(authoredOn) // not explicitly required/defined in dataset but important for context
* insert ObligationRules(requester)
* insert ObligationRules(sender)
* insert ObligationRules(recipient)
* insert ObligationRules(reasonCode) // already 1..1 so may not be needed place under obligation but added for consistency


Invariant: cr-date-required
Description: "The date of the CommunicationRequest is expected to be captured either in the resource itself or in the Encounter in which the CommunicationRequest originated."
Severity: #error
Expression: "authoredOn.exists() or encounter.exists()"
 

Mapping: MapACPInformRelativesRequest
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPInformRelativesRequest
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "734" "Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken?"


Instance: ACP-InformRelativesRequest-Pat1
InstanceOf: ACPInformRelativesRequest
Title: "ACP Request to Inform Relatives - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "4dbg052d-570a-40e6-b3a8-0c48347747f2"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #active // either 'active' or 'completed' depending on whether the communication has taken place yet
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* authoredOn = "2020-10-01"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter on 01-10-2020"
* requester = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* sender = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
//* recipient = "RelatedPerson xyz or family" // if there are known related persons they can be referenced here otherwise left out completely
* reasonCode = $snomed#713603004 "advance care planning"


Instance: ACP-InformRelativesRequest-Pat2
InstanceOf: ACPInformRelativesRequest
Title: "ACP Request to Inform Relatives - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c9736fd7-467c-497f-9235-d4efa8d46a34"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #completed 
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* authoredOn = "2025-08-07"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter on 07-08-2025"
* requester = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* sender = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* recipient = Reference(ACP-ContactPerson-GertJanDeJong-Pat2) "ContactPerson, Gert-Jan de Jong"
* reasonCode = $snomed#713603004 "advance care planning"
Profile: ACPInformRelativesRequest
Parent: CommunicationRequest
Id: ACP-InformRelativesRequest
Title: "ACP Request to Inform Relatives"
Description: "A CommunicationRequest representing the advice or instruction given to the patient to discuss their advance care planning (ACP) and treatment agreements with their relatives or proxies."
* insert MetaRules
* category 1..*
* category = $snomed#223449006
* requester only Reference(ACPHealthProfessionalPractitionerRole or ACPHealthProfessionalPractitioner) 
* sender only Reference(ACPPatient)
* recipient only Reference(ACPContactPerson)
* reasonCode 1..*
* reasonCode = $snomed#713603004 // "advance care planning"
* insert ObligationRules(category)
* insert ObligationRules(requester)
* insert ObligationRules(sender)
* insert ObligationRules(recipient)
* insert ObligationRules(reasonCode)
* insert ObligationRules(encounter)

Mapping: MapACPCommunicationRequest
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPInformRelativesRequest
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "734" "Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken?"


Instance: F1-ACP-CommunicationRequest-01-10-2020
InstanceOf: ACPInformRelativesRequest
Title: "F1 ACP CommunicationRequest"
Usage: #example

* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #active // either 'active' or 'completed' depending on whether the communication has taken place yet
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* authoredOn = "2020-10-01"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter on 01-10-2020"
* requester = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* sender = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
//* recipient = "RelatedPerson xyz or family" // if there are known related persons they can be referenced here otherwise left out completely
* reasonCode = $snomed#713603004 "advance care planning"
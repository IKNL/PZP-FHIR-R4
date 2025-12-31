Instance: P2-ACP-InformRelativesRequest-07-08-2025
InstanceOf: ACPInformRelativesRequest
Title: "P2 ACP InformRelativesRequest 07-08-2025"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c9736fd7-467c-497f-9235-d4efa8d46a34"
* category = $snomed#223449006 "adviseren om iemand te informeren" 
* category.text = "Request for patient to inform relatives about treatment agreements"
* status = #completed 
* subject = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* authoredOn = "2025-08-07"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter on 07-08-2025"
* requester = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* sender = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* recipient = Reference(P2-ACP-ContactPerson-GertJanDeJong) "ContactPerson, Gert-Jan de Jong"
* reasonCode = $snomed#713603004 "advance care planning"
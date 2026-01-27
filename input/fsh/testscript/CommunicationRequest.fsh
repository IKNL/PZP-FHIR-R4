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
* requester = Reference(ACP-HealthProfessionalPractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* sender = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* recipient = Reference(ACP-ContactPerson-GertJanDeJong-Pat2) "ContactPerson, Gert-Jan de Jong"
* reasonCode = $snomed#713603004 "advance care planning"
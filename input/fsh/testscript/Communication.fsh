Instance: P2-ACP-Communication-07-08-2025
InstanceOf: ACP-Communication
Title: "P2 ACP Communication"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c9736fd7-467c-497f-9235-d4efa8d46a34"
* topic = $snomed#223449006 "Recommendation to inform someone (procedure)"
* topic.text = "Informing the patient about their own responsibility to discuss these treatment agreements with relatives."
* status = #completed
* sent = "2025-08-07"
* subject = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* recipient = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* sender = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* reasonCode = $snomed#713603004 "Advance care planning (procedure)"

Instance: P1-ACP-Communication-29-07-2025
InstanceOf: ACPCommunication
Title: "P1 ACP Communication"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "db919dcf-5fa0-428a-b9a9-f1d7d86532d7"
* status = #completed
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* topic = $snomed#223449006 "Recommendation to inform someone (procedure)"
* topic.text = "Informing the patient about their own responsibility to discuss these treatment agreements with relatives."
* sent = "2025-07-29"
* recipient = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* sender = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* reasonCode = $snomed#713603004 "Advance care planning (procedure)"
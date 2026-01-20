Instance: P2-ACP-Procedure-07-08-2025
InstanceOf: ACP-Procedure
Title: "P2 ACP Procedure 07-08-2025"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e2efbdd1-b926-46c1-a18c-f72b4b281fbc"
* status = #completed
* subject = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(P2-ACP-ContactPerson-MayaVanDerSluijsMulder) "ContactPerson, Maya van der Sluijs"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2025-08-07"
* performedPeriod.end = "2025-08-07"
* code = $snomed#713603004 "advance care planning"

Instance: P2-ACP-Procedure-28-07-2024
InstanceOf: ACP-Procedure
Title: "P2 ACP Procedure 28-07-2024"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f527654a-5fa4-4394-95bc-50a9f50a5b1f"
* status = #completed
* subject = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(P2-ACP-ContactPerson-GertJanDeJong) "ContactPerson, Gert-Jan de Jong"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2024-07-28"
* performedPeriod.end = "2024-07-28"
* code = $snomed#713603004 "advance care planning"
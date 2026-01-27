Instance: ACP-AdvanceCarePlanningProcedure-1-Pat2
InstanceOf: ACP-Procedure
Title: "ACP Advance Care Planning Procedure - 1 - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e2efbdd1-b926-46c1-a18c-f72b4b281fbc"
* status = #completed
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(ACP-HealthProfessionalPractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-MayaVanDerSluijsMulder-Pat2) "ContactPerson, Maya van der Sluijs"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2025-08-07"
* performedPeriod.end = "2025-08-07"
* code = $snomed#713603004 "advance care planning"

Instance: ACP-AdvanceCarePlanningProcedure-2-Pat2
InstanceOf: ACP-Procedure
Title: "ACP Advance Care Planning Procedure - 2 - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f527654a-5fa4-4394-95bc-50a9f50a5b1f"
* status = #completed
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(ACP-HealthProfessionalPractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-GertJanDeJong-Pat2) "ContactPerson, Gert-Jan de Jong"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2024-07-28"
* performedPeriod.end = "2024-07-28"
* code = $snomed#713603004 "advance care planning"
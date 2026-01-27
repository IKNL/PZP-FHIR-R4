Instance: ACP-Encounter-1-Pat2
InstanceOf: ACP-Encounter
Title: "ACP Encounter - 1 -  Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ba69d05c-85d2-4773-8db4-4eb69d12d110"
* status = #finished
* class = $v3-ActCode#IMP "inpatient encounter"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* participant[0].individual = Reference(ACP-HealthProfessionalPractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* participant[=].individual.type = "PractitionerRole"
* participant[+].individual = Reference(ACP-ContactPerson-MayaVanDerSluijsMulder-Pat2) "ContactPerson, Maya van der Sluijs"
* participant[=].individual.type = "RelatedPerson"
* period.start = "2025-08-07"
* period.end = "2025-08-07"
* reasonReference = Reference(ACP-AdvanceCarePlanningProcedure-1-Pat2) "Procedure, ACP"
* reasonReference.extension[commentContactReason].url = "http://nictiz.nl/fhir/StructureDefinition/ext-Comment"
* reasonReference.extension[commentContactReason].valueString = "Derde PZP gesprek van mevrouw" 

Instance: ACP-Encounter-2-Pat2
InstanceOf: ACP-Encounter
Title: "ACP Encounter - 2 - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "4fd4a47f-e5a2-410d-8f3b-10bd58539013"
* status = #finished
* class = $v3-ActCode#IMP "inpatient encounter"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* participant[0].individual = Reference(ACP-HealthProfessionalPractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* participant[=].individual.type = "PractitionerRole"
* participant[+].individual = Reference(ACP-ContactPerson-GertJanDeJong-Pat2) "ContactPerson, Gert-Jan de Jong"
* participant[=].individual.type = "RelatedPerson"
* period.start = "2024-07-28"
* period.end = "2024-07-28"
* reasonReference = Reference(ACP-AdvanceCarePlanningProcedure-2-Pat2) "Procedure, ACP"
* reasonReference.extension[commentContactReason].url = "http://nictiz.nl/fhir/StructureDefinition/ext-Comment"
* reasonReference.extension[commentContactReason].valueString = "Eerste PZP gesprek van mevrouw " 
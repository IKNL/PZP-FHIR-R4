Instance: P2-ACP-Encounter-07-08-2025
InstanceOf: ACP-Encounter
Title: "P2 ACP Encounter 07-08-2025"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ba69d05c-85d2-4773-8db4-4eb69d12d110"
* status = #finished
* class = $v3-ActCode#IMP "Inpatient"
* subject = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
* participant[0].individual = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* participant[=].individual.type = "PractitionerRole"
* participant[+].individual = Reference(P2-ACP-ContactPerson-MayaVanDerSluijsMulder) "ContactPerson, Maya van der Sluijs"
* participant[=].individual.type = "RelatedPerson"
* period.start = "2025-08-07"
* period.end = "2025-08-07"
* reasonReference = Reference(P2-ACP-Procedure-07-08-2025) "Procedure, ACP"
* reasonReference.extension[commentContactReason].url = "http://nictiz.nl/fhir/StructureDefinition/ext-Comment"
* reasonReference.extension[commentContactReason].valueString = "Derde PZP gesprek van mevrouw" 
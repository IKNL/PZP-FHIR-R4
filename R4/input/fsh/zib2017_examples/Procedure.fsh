Instance: P1-ACP-Procedure-29-07-2025
InstanceOf: ACPProcedure
Title: "P1 ACP ACPProcedure 29-07-2025"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "6b384331-b19f-42a8-a7d7-2e5837d136e9"
* status = #completed
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer[0].actor = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(P1-ACP-ContactPerson-MichielHartman) "ContactPerson, Michiel Hartman"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2025-07-29"
* performedPeriod.end = "2025-07-29"




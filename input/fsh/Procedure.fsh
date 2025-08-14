Profile: ACPProcedure
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Procedure-event
Id: ACP-Procedure
Title: "Advance Care Planning Procedure"
Description: "Advance Care Planning procedure. Based on nl-core-Procedure-event profile and HCIM Procedure."
* insert MetaRules
* subject only Reference(ACPPatient)
* encounter only Reference(ACPEncounter)
* performer.actor only Reference(ACPHealthProfessionalPractitionerRole or ACPContactPerson or ACPPatient)
* code 1..1
* code = $snomed#713603004 "Advance care planning (procedure)"


Mapping: MapACPProcedure
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPProcedure
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "820" "Verrichting"
* code -> "827" "PZP gesprek (VerrichtingType)"

Instance: F1-ACP-Procedure-01-10-2020
InstanceOf: ACPProcedure
Title: "F1 ACP ACPProcedure 01-10-2020"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "64627bfa-f127-4d3a-2387-39426d7937dc"
* status = #completed 
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer[0].actor = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(F1-ACP-ContactPerson-HendrikHartman) "ContactPerson, Michiel Hartman"
* performer[=].actor.type = "ContactPerson"
* performer[+].actor = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2020-10-01"
* performedPeriod.end = "2020-10-01"



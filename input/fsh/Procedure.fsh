Profile: ACPProcedure
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Procedure-event
Id: ACP-Procedure
Title: "ACP Procedure"
Description: "Advance Care Planning procedure. Based on nl-core-Procedure-event profile and HCIM Procedure."
* insert MetaRules
* subject only Reference(ACPPatient)
* encounter only Reference(ACPEncounter)
* code 1..1
* code = $snomed#713603004

* insert ObligationRules(subject)
* insert ObligationRules(encounter)
* insert ObligationRules(code)

Mapping: MapACPProcedure
Id: pall-izppz-zib2020v2026-02-24
Title: "ACP dataset"
Source: ACPProcedure
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-02-24T09:29:59"
* -> "820" "Verrichting"
* code -> "827" "PZP gesprek (VerrichtingType)"


Instance: ACP-Procedure-Pat1
InstanceOf: ACPProcedure
Title: "ACP Procedure - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "64627bfa-f127-4d3a-2387-39426d7937dc"
* status = #completed 
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 01-10-2020"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer[0].actor = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-MichielHartman-Pat1) "ContactPerson, Michiel Hartman"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer[=].actor.type = "Patient"
* performedPeriod.start = "2020-10-01"
* performedPeriod.end = "2020-10-01"
* code = $snomed#713603004 "advance care planning"


Instance: ACP-Procedure-1-Pat2
InstanceOf: ACPProcedure
Title: "ACP Procedure - 1 - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e2efbdd1-b926-46c1-a18c-f72b4b281fbc"
* status = #completed
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-MayaVanDerSluijsMulder-Pat2) "ContactPerson, Maya van der Sluijs"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2025-08-07"
* performedPeriod.end = "2025-08-07"
* code = $snomed#713603004 "advance care planning"

Instance: ACP-Procedure-2-Pat2
InstanceOf: ACPProcedure
Title: "ACP Procedure - 2 - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f527654a-5fa4-4394-95bc-50a9f50a5b1f"
* status = #completed
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[0].actor = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* performer[=].actor.type = "PractitionerRole"
* performer[+].actor = Reference(ACP-ContactPerson-GertJanDeJong-Pat2) "ContactPerson, Gert-Jan de Jong"
* performer[=].actor.type = "RelatedPerson"
* performer[+].actor = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer[=].actor.type = "Patient" 
* performedPeriod.start = "2024-07-28"
* performedPeriod.end = "2024-07-28"
* code = $snomed#713603004 "advance care planning"

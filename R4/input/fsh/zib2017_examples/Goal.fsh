Instance: P1-ACP-Medical-Policy-Goal
InstanceOf: ACPMedicalPolicyGoal
Title: "P1 ACP Medical Policy Goal - Symptom management"
Usage: #example
* extension[encounter].valueReference = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ecd53b68-d9d2-4945-b1f0-0eccb07f48a3"
* lifecycleStatus = #active
* description = $snomed#713148004 "Symptom management (procedure)"
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* statusDate = "2025-07-29"
* note.text = "De behandeling van Hendrik is na verslechtering en gesprekken hierover bijgesteld van levensverlenging naar symptoomgericht"
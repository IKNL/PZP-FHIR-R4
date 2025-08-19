Instance: P2-ACP-Medical-Policy-Goal
InstanceOf: ACP-Medical-Policy-Goal
Title: "P2 ACP Medical Policy Goal - Life-sustaining treatment"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "b3aaf1a9-cbe3-4b7a-a6c8-ecc55a65e5e9"
* extension[encounter].valueReference = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* lifecycleStatus = #active
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* description = $snomed#713148004 " Symptom management (procedure)"
* statusDate = "2025-08-07"

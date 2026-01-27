Instance: ACP-MedicalPolicyGoal-Pat2
InstanceOf: ACP-Medical-Policy-Goal
Title: "ACP Medical Policy Goal - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "b3aaf1a9-cbe3-4b7a-a6c8-ecc55a65e5e9"
* lifecycleStatus = #active
* category = $snomed#713603004 "advance care planning"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* description = $snomed#713148004 "voorkomen en behandelen van symptomen"
* statusDate = "2025-08-07"

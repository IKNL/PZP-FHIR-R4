Instance: P1-ACP-MedicalDevice-ICD
InstanceOf: ACP-MedicalDevice
Title: "P1 ACP MedicalDevice ICD"
Usage: #example
* extension[healthProfessional].valueReference = Reference(P1-ACP-HealthProfessional-PractitionerRole-Santos) "Healthcare professional, Santos"
// * extension[location].valueReference = Reference(P1-ACP-Healthcareprovider-Location) "Healthcare provider (location), Zorginstelling F"
* extension[encounter].valueReference = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "19f6c62e-dc54-46ff-b350-99f1e7a5a566"
* status = #active
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* device = Reference(P1-ACP-MedicalDevice.Product-ICD)
// What to do with reference to problem as in test script? --> check with Esther
* bodySite = $snomed#80891009 "Heart structure (body structure)"
* bodySite.extension[laterality].valueCodeableConcept = $snomed#7771000 "Links"
* timingPeriod.start = "2020-05-19"

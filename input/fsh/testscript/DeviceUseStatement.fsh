Instance: P2-ACP-MedicalDevice-ICD
InstanceOf: ACPMedicalDevice
Title: "P2 ACP MedicalDevice ICD"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "3fdc0ec5-2984-4b47-b6b8-f9822fb8c425"
* extension[healthProfessional].valueReference = Reference(P2-ACP-HealthProfessional2-PractitionerRole-Santos) "Healthcare professional, Santos"
* extension[encounter].valueReference = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* device = Reference(P2-ACP-MedicalDevice.Product-ICD)
* status = #active
* timingPeriod.start = "2024"
* bodySite.coding = $snomed#80891009 "Heart structure (body structure)"
* bodySite.extension[laterality].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AnatomicalLocation.Laterality"
* bodySite.extension[laterality].valueCodeableConcept.coding = $snomed#7771000 "Left (qualifier value)"
* note.text = "ICD is ongeveer eén jaar geleden geïmplanteerd."


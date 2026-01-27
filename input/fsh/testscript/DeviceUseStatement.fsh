Instance: ACP-MedicalDevice-ICD-Pat2
InstanceOf: ACPMedicalDevice
Title: "ACP MedicalDevice - ICD - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "3fdc0ec5-2984-4b47-b6b8-f9822fb8c425"
* extension[healthProfessional].valueReference = Reference(ACP-HealthProfessionalPractitionerRole-Santos-Pat2) "Healthcare professional, Santos"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* device = Reference(ACP-MedicalDeviceProduct-ICD-Pat2)
* status = #active
* timingPeriod.start = "2024"
* bodySite.coding = $snomed#80891009 "structuur van cor"
* bodySite.extension[laterality].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AnatomicalLocation.Laterality"
* bodySite.extension[laterality].valueCodeableConcept.coding = $snomed#7771000 "links"
* note.text = "ICD is ongeveer eén jaar geleden geïmplanteerd."


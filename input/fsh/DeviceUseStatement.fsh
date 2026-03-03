Profile: ACPMedicalDevice
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice
Id: ACP-MedicalDevice
Title: "ACP MedicalDevice"
Description: "Any internally implanted and external devices and/or aids used by the patient (in the past) to reduce the effects of functional limitations in organ systems or to facilitate the treatment of a disease. In the context of ACP, this profile is used to declare the use of an implantable cardioverter defibrillator (ICD). Based on nl-core-MedicalDevice and HCIM MedicalDevice."
* insert MetaRules
* subject only Reference(ACPPatient)
* device only Reference(ACPMedicalDeviceProductICD or http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product)

* insert ObligationRules(extension[healthProfessional])
* insert ObligationRules(extension[location])
* insert ObligationRules(subject)
* insert ObligationRules(device)
* insert ObligationRules(timingPeriod.start)
* insert ObligationRules(timingPeriod.end)
* insert ObligationRules(reasonReference[indication])
* insert ObligationRules(bodySite)
* insert ObligationRules(bodySite.extension[laterality])
* insert ObligationRules(note.text)

Mapping: MapACPMedicalDevice
Id: pall-izppz-zib2020v2026-02-24
Title: "ACP dataset"
Source: ACPMedicalDevice
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-02-24T09:29:59"
* -> "619" "Heeft de patient een ICD?"
* -> "620" "ICD (MedischHulpmiddel)"
* extension[healthProfessional]  -> "635" "Zorgverlener"
* extension[location]  -> "633" "Locatie"
* timingPeriod.start -> "630" "BeginDatum"
* timingPeriod.end -> "631" "EndDate"
* reasonReference[indication] -> "628" "Indicatie"
* bodySite -> "625" "AnatomischeLocatie"
* bodySite -> "626" "Locatie"
* bodySite.extension[laterality] -> "627" "Lateraliteit"
* note.text -> "632" "Toelichting"


Instance: ACP-MedicalDevice-ICD-Pat1
InstanceOf: ACPMedicalDevice
Title: "ACP MedicalDevice - ICD - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "99a671c0-f756-4c29-bba2-ad8d6f05a5fe"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* device = Reference(ACP-MedicalDeviceProduct-ICD-Pat1)
* status = #active
* timingPeriod.start = "2018"
* note.text = "Geïmplanteerd in 2018"


Instance: ACP-MedicalDevice-ICD-Pat2
InstanceOf: ACPMedicalDevice
Title: "ACP MedicalDevice - ICD - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "3fdc0ec5-2984-4b47-b6b8-f9822fb8c425"
* extension[healthProfessional].valueReference = Reference(ACP-HealthProfessional-PractitionerRole-Santos-Pat2) "Healthcare professional, Santos"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* device = Reference(ACP-MedicalDeviceProduct-ICD-Pat2)
* status = #active
* timingPeriod.start = "2024"
* bodySite.coding = $snomed#80891009 "structuur van cor"
* bodySite.extension[laterality].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AnatomicalLocation.Laterality"
* bodySite.extension[laterality].valueCodeableConcept.coding = $snomed#7771000 "links"
* note.text = "ICD is ongeveer eén jaar geleden geïmplanteerd."
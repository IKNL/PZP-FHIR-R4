Profile: ACPMedicalDevice
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice
Id: ACP-MedicalDevice
Title: "MedicalDevice"
Description: "Medical devices are any internally implanted and external devices and/or aids used by the patient (in the past) to reduce the effects of functional limitations in organ systems or to facilitate the treatment of a disease."
* insert MetaRules
* extension contains
    ExtEncounterReference  named encounter 0..1
* extension[encounter].valueReference only Reference(ACPEncounter) 
* subject only Reference(ACPPatient)
* device only Reference(ACPMedicalDeviceProductICD or http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product)

Mapping: MapACPMedicalDevice
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPMedicalDevice
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "619" "Heeft de patient een ICD?"
* -> "620" "ICD (MedischHulpmiddel)"
* extension[healthProfessional].value[x]  -> "635" "Zorgverlener"
* extension[location].value[x]  -> "633" "Locatie"
* timingPeriod.start -> "630" "BeginDatum"
* timingPeriod.end -> "631" "EndDate"
* reasonReference[indication] -> "628" "Indicatie"
* bodySite -> "625" "AnatomischeLocatie"
* bodySite -> "626" "Locatie"
* bodySite.extension[laterality].valueCodeableConcept -> "627" "Lateraliteit"
* note.text -> "632" "Toelichting"

Instance: F1-ACP-MedicalDevice-ICD
InstanceOf: ACPMedicalDevice
Title: "F1 ACP MedicalDevice ICD"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "99a671c0-f756-4c29-bba2-ad8d6f05a5fe"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* device = Reference(F1-ACP-MedicalDevice.Product-ICD)
* status = #active
* timingPeriod.start = "2018"
* note.text = "Geïmplanteerd in 2018"
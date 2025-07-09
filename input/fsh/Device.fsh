Profile: ACPMedicalDeviceProductICD
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product
Id: ACP-MedicalDevice.Product-ICD
Title: "ACP MedicalDevice Product ICD"
Description: " TODO"
* insert MetaRules
* type from ACPProductTypeICDVS (required)


Mapping: MapACPMedicalDeviceProductICD
Id: pall-izppz-v2025-03-11
Title: "ICD (MedischHulpmiddel)"
Source: ACPMedicalDeviceProductICD
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "620" "ICD (MedischHulpmiddel)"
* identifier[gs1ProductID] -> "622" "ProductID"
* identifier[hibcProductID] -> "622" "ProductID"
* udiCarrier[gs1UdiCarrier].carrierHRF -> "622" "ProductID"
* udiCarrier[hibcUdiCarrier].carrierHRF -> "622" "ProductID"
* type -> "623" "ProductType van ICD"
* note.text -> "624" "ProductOmschrijving"


Instance: F1-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "MedicalDevice.Product ICD"
Usage: #example
* type = $snomed#72506001 "Implantable defibrillator, device (physical object)"
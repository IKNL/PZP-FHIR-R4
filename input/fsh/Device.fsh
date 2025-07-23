Profile: ACPMedicalDeviceProductICD
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product
Id: ACP-MedicalDevice.Product-ICD
Title: "MedicalDevice Product ICD"
Description: "ICD MedicalDevice Product."
* insert MetaRules
* type from ACPMedicalDeviceProductTypeICDVS (required)


Mapping: MapACPMedicalDeviceProductICD
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPMedicalDeviceProductICD
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* identifier[gs1ProductID] -> "622" "ProductID"
* identifier[hibcProductID] -> "622" "ProductID"
* udiCarrier[gs1UdiCarrier].carrierHRF -> "622" "ProductID"
* udiCarrier[hibcUdiCarrier].carrierHRF -> "622" "ProductID"
* type -> "623" "ProductType van ICD"
* type -> "619" "Heeft de patient een ICD?"
* note.text -> "624" "ProductOmschrijving"


Instance: F1-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "F1 ACP MedicalDevice.Product ICD"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "00e66024-84a5-44f8-84e9-f8ac339bfd5a"
* type = $snomed#72506001 "Implantable defibrillator, device (physical object)"
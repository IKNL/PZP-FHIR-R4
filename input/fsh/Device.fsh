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
* -> "621" "Product"
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

Instance: P2-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "P2 ACP MedicalDevice.Product ICD"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "7b04eb93-0d7b-41ed-84d1-d9012696b81e"
* identifier[gs1ProductID].system = "https://www.gs1.org/gtin"
* identifier[gs1ProductID].value = "8700000000001"
* type = $snomed#72506001 "Implantable defibrillator, device (physical object)"
// Probleem en zorgaanbieder niet meegenomen omdat deze niet zijn gedefinieerd in losse profielen 
// klopt het dat de gs1 code een product ID is en niet een udi carrier?
// Bij device staat een referentie naar een healthcare professional, hier staat de nl core healthcare professional, daar kan ik in principe ook een ACP healtcare professsional aan toevoegen omdat die overerft uit de NL core of gaat dat fout? 


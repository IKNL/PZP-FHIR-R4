Profile: ACPMedicalDeviceProductICD
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product
Id: ACP-MedicalDevice.Product-ICD
Title: "MedicalDevice Product ICD"
Description: "The medical device (internally or externally). In the context of ACP, this profile is used to capture information on a patient's implantable cardioverter defibrillator (ICD). Based on nl-core-MedicalDeviceProduct and HCIM MedicalDevice."
* insert MetaRules
* type from ACPMedicalDeviceProductTypeICDVS (required)


Mapping: MapACPMedicalDeviceProductICD
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPMedicalDeviceProductICD
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
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
* type = $snomed#465460004 "univentriculaire implanteerbare hartdefibrillator"
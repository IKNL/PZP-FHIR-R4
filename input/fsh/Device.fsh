Profile: ACPMedicalDeviceProductICD
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice.Product
Id: ACP-MedicalDevice.Product-ICD
Title: "ACP MedicalDevice Product ICD"
Description: "The medical device (internally or externally). In the context of ACP, this profile is used to capture information on a patient's implantable cardioverter defibrillator (ICD). Based on nl-core-MedicalDeviceProduct and HCIM MedicalDevice."
* insert MetaRules
* type from ACPMedicalDeviceProductTypeICDVS (required)

* insert ObligationRules(identifier[gs1ProductID])
* insert ObligationRules(identifier[hibcProductID])
* insert ObligationRules(udiCarrier[gs1UdiCarrier].carrierHRF)
* insert ObligationRules(udiCarrier[hibcUdiCarrier].carrierHRF)
* insert ObligationRules(type)
* insert ObligationRules(note.text)


Mapping: MapACPMedicalDeviceProductICD
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPMedicalDeviceProductICD
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "621" "Product"
* identifier[gs1ProductID] -> "622" "ProductID"
* identifier[hibcProductID] -> "622" "ProductID"
* udiCarrier[gs1UdiCarrier].carrierHRF -> "622" "ProductID"
* udiCarrier[hibcUdiCarrier].carrierHRF -> "622" "ProductID"
* type -> "623" "ProductType van ICD"
* type -> "619" "Heeft de patient een ICD?"
* note.text -> "624" "ProductOmschrijving"


Instance: ACP-MedicalDeviceProduct-ICD-Pat1
InstanceOf: ACPMedicalDeviceProductICD
Title: "ACP MedicalDevice Product ICD - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "00e66024-84a5-44f8-84e9-f8ac339bfd5a"
* type = $snomed#72506001 "implanteerbare cardioverter-defibrillator"


Instance: ACP-MedicalDeviceProduct-ICD-Pat2
InstanceOf: ACPMedicalDeviceProductICD
Title: "ACP MedicalDevice Product ICD - Pat 2"
Usage: #example
* identifier[gs1ProductID].system = "https://www.gs1.org/gtin"
* identifier[gs1ProductID].value = "8700000000001"
* type = $snomed#72506001 "implanteerbare cardioverter-defibrillator"
// Probleem en zorgaanbieder niet meegenomen omdat deze niet zijn gedefinieerd in losse profielen 
// klopt het dat de gs1 code een product ID is en niet een udi carrier?
// Bij device staat een referentie naar een healthcare professional, hier staat de nl core healthcare professional, daar kan ik in principe ook een ACP healtcare professsional aan toevoegen omdat die overerft uit de NL core of gaat dat fout? 
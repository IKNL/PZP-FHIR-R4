Instance: P1-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "P1 ACP MedicalDevice.Product ICD"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "aada7cbf-d39d-4ace-85aa-05a311b9adc2"
* identifier[gs1ProductID].system = "https://www.gs1.org/gtin"
* identifier[gs1ProductID].value = "8700000000000"
* udiCarrier[gs1UdiCarrier].issuer = "https://www.gs1.org/gtin"
* udiCarrier[gs1UdiCarrier].carrierHRF = "8700000000000"
// use both identifier and udiCarrier?
* type = $snomed#72506001 "Implantable defibrillator, device (physical object)"
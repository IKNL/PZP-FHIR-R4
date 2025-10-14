Instance: P1-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "P1 ACP MedicalDevice.Product ICD"
Usage: #example
* identifier[gs1ProductID].system = "https://www.gs1.org/gtin"
* identifier[gs1ProductID].value = "8700000000000"
* udiCarrier[gs1UdiCarrier].issuer = "https://www.gs1.org/gtin"
* udiCarrier[gs1UdiCarrier].carrierHRF = "8700000000000"
* type = $snomed#72506001 "implanteerbare hartdefibrillator"
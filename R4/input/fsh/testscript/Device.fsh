Instance: P2-ACP-MedicalDevice.Product-ICD
InstanceOf: ACPMedicalDeviceProductICD
Title: "P2 ACP MedicalDevice.Product ICD"
Usage: #example
* identifier[gs1ProductID].system = "https://www.gs1.org/gtin"
* identifier[gs1ProductID].value = "8700000000001"
* type = $snomed#72506001 "Implantable defibrillator, device (physical object)"
// Probleem en zorgaanbieder niet meegenomen omdat deze niet zijn gedefinieerd in losse profielen 
// klopt het dat de gs1 code een product ID is en niet een udi carrier?
// Bij device staat een referentie naar een healthcare professional, hier staat de nl core healthcare professional, daar kan ik in principe ook een ACP healtcare professsional aan toevoegen omdat die overerft uit de NL core of gaat dat fout? 


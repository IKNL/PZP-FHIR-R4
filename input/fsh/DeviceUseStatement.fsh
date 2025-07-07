Profile: ACPMedicalDevice
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-MedicalDevice
Id: ACP-MedicalDevice
Title: "ACP MedicalDevice"
Description: "Medical devices are any internally implanted and external devices and/or aids used by the patient (in the past) to reduce the effects of functional limitations in organ systems or to facilitate the treatment of a disease."
* insert MetaRules
* subject only Reference(ACPPatient)
* device only Reference(ACPMedicalDeviceProductICD or Device)

Mapping: MapACPMedicalDevice
Id: pall-izppz-v2025-03-11
Title: "ICD (MedischHulpmiddel)"
Source: ACPMedicalDevice
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "620" "ICD (MedischHulpmiddel)"
* extension[healthProfessional] -> "635" "Zorgverlener"
* extension[location] -> "633" "Locatie"
* timingPeriod.start -> "630" "BeginDatum"
* timingPeriod.end -> "631" "EndDate"
* reasonReference[indication] -> "628" "Indicatie"
* bodySite -> "625" "AnatomischeLocatie"
* note.text -> "632" "Toelichting"


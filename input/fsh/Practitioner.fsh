Profile: ACPHealthProfessionalPractitioner
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner
Id: ACP-HealthProfessional-Practitioner
Title: "ACP Practitioner"
Description: "In the context of Advance Care Planning (ACP), a Practitioner refers to a healthcare professional who engages in discussions and makes agreements with the Patient and/or their Legal Representative. Depending on the specific stage or pathway of the ACP process, multiple Practitioners may be involved, each responsible for facilitating conversations and documenting decisions in accordance with their role."
* insert MetaRules
// TODO: check if uzi and agb are correct to label as mustSupport -- they are not mentioned in dataset
* identifier[uzi] ^sliceName = "uzi"
* identifier[uzi] ^mustSupport = true
* identifier[agb] ^sliceName = "agb"
* identifier[agb] ^mustSupport = true
* name[nameInformation] ^sliceName = "nameInformation"
// TODO: check if these mustSupports are correct
* name[nameInformation].family.extension[prefix] ^sliceName = "prefix"
* name[nameInformation].family.extension[prefix] ^mustSupport = true
* name[nameInformation].family.extension[lastName] ^sliceName = "lastName"
* name[nameInformation].family.extension[lastName] ^mustSupport = true
* name.given MS

Mapping: MapACPHealthProfessionalPractitioner
Id: pall-izppz-v2025-03-11
Title: "Gesprek gevoerd door (Zorgverlener)"
Source: ACPHealthProfessionalPractitioner
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* identifier -> "392" "ZorgverlenerIdentificatienummer"
* name[nameInformation-GivenName].given -> "394" "Voornamen"
* name[nameInformation].family -> "398" "Geslachtsnaam"
* name[nameInformation].family.extension[prefix] -> "399" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "400" "Achternaam"


Instance: F1-ACP-HealthProfessional-Practitioner-DrVanHuissen
InstanceOf: ACPHealthProfessionalPractitioner
Title: "Dr. van Huissen"
Usage: #example
* name.use = #official
* name.text = "van Huissen"
* name.family = "van Huissen"
* name.family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name.family.extension[=].valueString = "van"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension[=].valueString = "Huissen"
* name.prefix = "Dr."
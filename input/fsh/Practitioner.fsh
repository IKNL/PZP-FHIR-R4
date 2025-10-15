Profile: ACPHealthProfessionalPractitioner
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner
Id: ACP-HealthProfessional-Practitioner
Title: "HealthProfessional Practitioner"
Description: "A person who is authorized to perform actions in the field of individual healthcare. Based on nl-core-HealthProfessionalPractitioner and HCIM HealthProfessional."
* insert MetaRules


Mapping: MapACPHealthProfessionalPractitioner
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPHealthProfessionalPractitioner
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* identifier -> "392" "ZorgverlenerIdentificatienummer"
* name -> "393" "Naamgegevens"
* name[nameInformation-GivenName].given -> "394" "Voornamen"
* name[nameInformation].family -> "398" "Geslachtsnaam"
* name[nameInformation].family.extension[prefix] -> "399" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "400" "Achternaam"


Instance: F1-ACP-HealthProfessional-Practitioner-DrVanHuissen
InstanceOf: ACPHealthProfessionalPractitioner
Title: "F1 ACP HealthProfessional Practitioner Dr. van Huissen"
Usage: #example
* identifier.system = "http://fhir.nl/fhir/NamingSystem/agb-z"
* identifier.value = "01999999"
* name.use = #official
* name.text = "van Huissen"
* name.family = "van Huissen"
* name.family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name.family.extension[=].valueString = "van"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension[=].valueString = "Huissen"
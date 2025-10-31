Profile: ACPHealthProfessionalPractitioner
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner
Id: ACP-HealthProfessional-Practitioner
Title: "HealthProfessional Practitioner"
Description: "A person who is authorized to perform actions in the field of individual healthcare. Based on nl-core-HealthProfessionalPractitioner and HCIM HealthProfessional."
* insert MetaRules
* insert ObligationRules(identifier)
* insert ObligationRules(name[nameInformation-GivenName].given)
* insert ObligationRules(name[nameInformation].family)
* insert ObligationRules(name[nameInformation].family.extension[prefix])
* insert ObligationRules(name[nameInformation].family.extension[lastName])


Mapping: MapACPHealthProfessionalPractitioner
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPHealthProfessionalPractitioner
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
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
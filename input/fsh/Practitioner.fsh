Profile: ACPHealthProfessionalPractitioner
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner
Id: ACP-HealthProfessional-Practitioner
Title: "ACP HealthProfessional Practitioner"
Description: "A person who is authorized to perform actions in the field of individual healthcare. Based on nl-core-HealthProfessionalPractitioner and HCIM HealthProfessional."
* insert MetaRules
* insert ObligationRules(identifier)
* insert ObligationRules(name[nameInformation-GivenName].given)
* insert ObligationRules(name[nameInformation].family)
* insert ObligationRules(name[nameInformation].family.extension[prefix])
* insert ObligationRules(name[nameInformation].family.extension[lastName])


Mapping: MapACPHealthProfessionalPractitioner
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPHealthProfessionalPractitioner
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-08-10T10%3A11%3A40"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* identifier -> "392" "ZorgverlenerIdentificatienummer"
* name -> "393" "Naamgegevens"
* name[nameInformation-GivenName].given -> "394" "Voornamen"
* name[nameInformation].family -> "398" "Geslachtsnaam"
* name[nameInformation].family.extension[prefix] -> "399" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "400" "Achternaam"


Instance: ACP-HealthProfessional-Practitioner-DrVanHuissen-Pat1
InstanceOf: ACPHealthProfessionalPractitioner
Title: "ACP HealthProfessional Practitioner - Dr. van Huissen - Pat 1"
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


Instance: ACP-HealthProfessional-Practitioner-DesireeWolters-Pat2
InstanceOf: ACPHealthProfessionalPractitioner
Title: "ACP HealthProfessional Practitioner - Desiree Wolters - Pat 2"
Usage: #example
* identifier.system = "http://fhir.nl/fhir/NamingSystem/agb-z"
* identifier.value = "000003333"
* name.use = #official
* name.text = "Desiree Wolters"
* name.family = "Wolters"
* name.family.extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension.valueString = "Wolters"
* name.given = "Desiree"
* name.given.extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name.given.extension.valueCode = #BR


Instance: ACP-HealthProfessional-Practitioner-Santos-Pat2
InstanceOf: ACPHealthProfessionalPractitioner
Title: "ACP HealthProfessional Practitioner - Santos - Pat 2"
Usage: #example
* name.use = #official
* name.text = "Richard Santos"
Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient
Id: ACP-Patient
Title: "Patient"
Description: "A person who receives medical, psychological, paramedical or nursing care."
* insert MetaRules
* name 1..* // In scenario Naamgegevens is 1..1, but because the zib nameinformation does not mapp 1..1 to FHIR we will set this to 1..* instead of 1..1
* name[nameInformation] ^sliceName = "nameInformation"
* name[nameInformation] 1..2
* name[nameInformation].family 1.. // TODO discuss with Lonneke what the correct cardinality is

Mapping: MapACPPatient
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPPatient
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "351" "Patient"
* identifier -> "385" "Identificatienummer"
* name -> "352" "Naamgegevens"
// TODO add complete ArtDecor mapping 
// * name[nameInformation-GivenName].given -> "358" "Voornamen"
// * name[nameInformation].family -> "357" "Geslachtsnaam"
* telecom -> "376" "Contactgegevens"
// TODO - HK contactgegevens is in de zib 0..1 en dataset 0..1 maar in nl core 0..* bespreken met lonneke 
* gender -> "387" "Geslacht"
* gender.extension[genderCodelist].value[x] -> "387" "Geslacht"
* birthDate -> "386" "Geboortedatum"
* address -> "364" "Adresgegevens"
* contact.extension[relatedPerson] -> "477" "Vertegenwoordiger is contactpersoon" // TODO check this mapping... should likely be in combination with the relationship coding urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24

Instance: F1-ACP-Patient-HendrikHartman
InstanceOf: ACPPatient
Title: "F1 ACP Patient Hendrik Hartman"
Usage: #example
* identifier.system = "http://fhir.nl/fhir/NamingSystem/bsn"
* identifier.value = "999911120"
* name[nameInformation].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[nameInformation].extension.valueCode = #NL1
* name[nameInformation].use = #official
* name[nameInformation].text = "Hendrik Hartman"
* name[nameInformation].family = "Hartman"
* name[nameInformation].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[nameInformation].family.extension[=].valueString = "Hartman"
* name[nameInformation].given[0] = "Hendrik"
* name[nameInformation].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation-GivenName].use = #usual
* name[nameInformation-GivenName].given = "Hendrik"
* birthDate = "1961-01-01"

* contact.extension[relatedPerson].valueReference = Reference(F1-ACP-ContactPerson-HendrikHartman)
* contact.relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* contact.relationship[+] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24 "Wettelijke vertegenwoordiger"
* contact.relationship[+] = $v3-RoleCode#BRO "brother"
* contact.name.extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* contact.name.extension.valueCode = #NL1
* contact.name.use = #official
* contact.name.text = "Michiel Hartman"
* contact.name.family = "Hartman"
* contact.name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* contact.name.family.extension[=].valueString = "Hartman"
* contact.name.given[0] = "Michiel"
* contact.name.given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* contact.name.given[=].extension.valueCode = #BR
* contact.telecom[0].system = #email
* contact.telecom[=].value = "michiel.hartman@iknl.nl"
* contact.telecom[=].use = #work
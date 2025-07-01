
Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient
Id: ACP-Patient
Title: "ACP Patient"
Description: "A person who receives medical, psychological, paramedical or nursing care."
* insert MetaRules
* name 1..* // In scenario Naamgegevens is 1..1, but because the zib nameinformation does not mapp 1..1 to FHIR we will set this to 1..* instead of 1..1
* name[nameInformation] ^sliceName = "nameInformation"
* name[nameInformation] 1..2
* name[nameInformation].family.extension[prefix] ^sliceName = "prefix"
* name[nameInformation].family 1..
* name[nameInformation].family.extension[prefix] ^mustSupport = true
* name[nameInformation].family.extension[lastName] ^sliceName = "lastName"
* name[nameInformation].family.extension[lastName] ^mustSupport = true

// TODO: need to rework this from STU3 
// * communication.extension[languageProficiency] ^sliceName = "languageProficiency"
// * communication.extension[languageProficiency].extension 2..
* communication.extension[languageControl] ^sliceName = "languageControl"
* communication.extension[languageControl] ^mustSupport = true

Mapping: MapACPPatient
Id: pall-izppz-v2025-03-11
Title: "Patient"
Source: ACPPatient
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "351" "Patient"
* identifier -> "385" "Identificatienummer"
* name -> "352" "Naamgegevens"
// TODO: decide if we want to go into providing mappings inside these data type profiles. 
// * name[nameInformation-GivenName].given -> "358" "Voornamen"
// * name[nameInformation].family -> "357" "Geslachtsnaam"
* telecom -> "376" "Contactgegevens"
* gender -> "387" "Geslacht"
* gender.extension[genderCodelist].value[x] -> "387" "Geslacht"
* birthDate -> "386" "Geboortedatum"
* address -> "364" "Adresgegevens"

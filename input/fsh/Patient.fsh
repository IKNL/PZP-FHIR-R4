
Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient
Id: ACP-Patient
Title: "ACP Patient"
Description: "[TO-DO]"
* insert MetaRules

* name ^mustSupport = false
* name[nameInformation] ^sliceName = "nameInformation"
* name[nameInformation] 1..1
* name[nameInformation].family.extension[prefix] ^sliceName = "prefix"
* name[nameInformation].family 1..
* name[nameInformation].family.extension[prefix] ^mustSupport = true
* name[nameInformation].family.extension[lastName] ^sliceName = "lastName"
* name[nameInformation].family.extension[lastName] ^mustSupport = true
* name.given MS
* birthDate MS

// need to rework this from STU3 
// * communication.extension[languageProficiency] ^sliceName = "languageProficiency"
// * communication.extension[languageProficiency].extension 2..
* communication.extension[languageControl] ^sliceName = "languageControl"
* communication.extension[languageControl] ^mustSupport = true


Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient
Id: ACP-Patient
Title: "Patient"
Description: "A person who receives medical, psychological, paramedical or nursing care."
* insert MetaRules
* obeys ACP-Patient-1
* extension contains
    ExtLegallyCapableTreatmentDecision  named LegallyCapableTreatmentDecision 0..1
* extension[LegallyCapableTreatmentDecision] ^condition = "ACP-Patient-1"
* name 1..* // TODO MM check kardinaliteit met Lonneke - In scenario Naamgegevens is 1..1, but because the zib nameinformation does not mapp 1..1 to FHIR we will set this to 1..* instead of 1..1
* name[nameInformation] ^sliceName = "nameInformation"
* name[nameInformation] 1..2
* name[nameInformation].family 1.. // TODO discuss with Lonneke what the correct cardinality is
* contact ^condition = "ACP-Patient-1"
* contact.relationship ^condition = "ACP-Patient-1"

Invariant: ACP-Patient-1
Description: "If the patient is not legally capable, there needs to be a legal representative"
* severity = #error
* expression = "extension.where(url='https://fhir.iknl.nl/fhir/StructureDefinition/ext-LegallyCapable-TreatmentDecision').where(url='legallyCapableComment').value = false implies contact.where(relationship.coding.code = '24').exists()" // TODO needs to be tested and TODO discuss with Lonneke if we need to add this to ARTDECOR too 
// TODO currently all the mappings are set inside relatedperson... perhaps the invariant should be set to check if there is a reference set to the relatedperson? Or duplicate mappings.

Mapping: MapACPPatient
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPPatient
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "351" "Patient"
* extension[LegallyCapableTreatmentDecision] -> "761" "Wilsbekwaamheid m.b.t. medische behandelbeslissingen" 
* extension[LegallyCapableTreatmentDecision].extension[legallyCapable].valueBoolean -> "762" "Wilsbekwaamheid m.b.t. medische behandelbeslissingen"
* extension[LegallyCapableTreatmentDecision].extension[legallyCapableComment].valueString -> "763" "Toelichting"
* identifier -> "385" "Identificatienummer"
* name -> "352" "Naamgegevens"
* name[nameInformation].given -> "353" "Voornamen"
* name[nameInformation].given -> "354" "Initialen"
* name[nameInformation-GivenName].given -> "355" "Roepnaam"
* name[nameInformation].use -> "356" "Naamgebruik"
// 357 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix].valueString -> "358" "Voorvoegsels"
* name[nameInformation].family.extension[lastName].valueString -> "359" "Achternaam"
// 360 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix].valueString -> "361" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName].valueString -> "362" "AchternaamPartner"
* name[nameInformation].suffix -> "363" "Titels"
* name -> "515" "Naamgegevens"
* name[nameInformation].given -> "516" "Voornamen"
* name[nameInformation].given -> "517" "Initialen"
* name[nameInformation-GivenName].given -> "518" "Roepnaam"
* name[nameInformation].use -> "519" "Naamgebruik"
// 520 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix].valueString -> "521" "Voorvoegsels"
* name[nameInformation].family.extension[lastName].valueString -> "522" "Achternaam"
// 523 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix].valueString -> "524" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName].valueString -> "525" "AchternaamPartner"
* name[nameInformation].suffix -> "526" "Titels"
* telecom -> "376" "Contactgegevens" // TODO - HK contactgegevens is in de zib 0..1 en dataset 0..1 maar in nl core 0..* bespreken met lonneke 
* telecom[telephoneNumbers] -> "377" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "378" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "379" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept -> "379" "TelecomType"
* telecom[telephoneNumbers].use -> "380" "NummerSoort"
* telecom[telephoneNumbers].extension[comment].valueString -> "381" "Toelichting"
* telecom[emailAddresses] -> "382" "EmailAdressen"
* telecom[emailAddresses].value -> "383" "EmailAdres"
* telecom[emailAddresses].system -> "384" "EmailSoort"
* gender -> "387" "Geslacht"
* gender.extension[genderCodelist].value[x] -> "387" "Geslacht" // TODO MM check binding codelijst
* birthDate -> "386" "Geboortedatum"
* address -> "364" "Adresgegevens"
* address.line.extension[streetName].valueString -> "365" "Straat"
* address.line.extension[houseNumber].valueString -> "366" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "367" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "368" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication].valueString -> "369" "AanduidingBijHuisnummer"
* address.postalCode -> "370" "Postcode"
* address.city -> "371" "Woonplaats"
* address.district -> "372" "Gemeente"
* address.country.extension[countryCode].valueCodeableConcept -> "373" "Land"
* address.line.extension[additionalInformation].valueString -> "374" "AdditioneleInformatie"
* address.use -> "375" "AdresSoort"
* address.type -> "375" "AdresSoort"
* contact.extension[relatedPerson] -> "477" "Vertegenwoordiger is contactpersoon" // TODO check this mapping... should likely be in combination with the relationship coding urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24

Instance: F1-ACP-Patient-HendrikHartman
InstanceOf: ACPPatient
Title: "F1 ACP Patient Hendrik Hartman"
Usage: #example
* extension[LegallyCapableTreatmentDecision].extension[legallyCapable].valueBoolean = true
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
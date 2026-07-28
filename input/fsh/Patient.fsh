Profile: ACPPatient
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Patient
Id: ACP-Patient
Title: "ACP Patient"
Description: "A person who receives medical, psychological, paramedical, or nursing care. Based on nl-core-Patient and HCIM Patient."
* insert MetaRules
* name 1..*
* contact.extension[relatedPerson] ^comment = "All information regarding the patient's contact persons should preferably be stored in the RelatedPerson resource, and optionally in `Patient.contact`. The http://hl7.org/fhir/StructureDefinition/patient-relatedPerson extension is used to link the contact person to the Patient and to emphasize that the related person is also a contact person of the patient."
* contact.extension[relatedPerson].valueReference only Reference(ACPContactPerson)


* insert ObligationRules(contact.extension[relatedPerson])
* insert ObligationRules(identifier)
* insert ObligationRules(name[nameInformation].given)
* insert ObligationRules(name[nameInformation-GivenName].given)
* insert ObligationRules(name[nameInformation].use)
* insert ObligationRules(name[nameInformation].family.extension[prefix])
* insert ObligationRules(name[nameInformation].family.extension[lastName])
* insert ObligationRules(name[nameInformation].family.extension[partnerPrefix])
* insert ObligationRules(name[nameInformation].family.extension[partnerLastName])
* insert ObligationRules(name[nameInformation].suffix)
* insert ObligationRules(telecom[telephoneNumbers].value)
* insert ObligationRules(telecom[telephoneNumbers].system)
* insert ObligationRules(telecom[telephoneNumbers].system.extension[telecomType])   
* insert ObligationRules(telecom[telephoneNumbers].use)
* insert ObligationRules(telecom[telephoneNumbers].extension[comment])
* insert ObligationRules(telecom[emailAddresses].value)
* insert ObligationRules(telecom[emailAddresses].system)    
* insert ObligationRules(gender) 
* insert ObligationRules(gender.extension[genderCodelist])   
* insert ObligationRules(birthDate)
* insert ObligationRules(address.line.extension[streetName])
* insert ObligationRules(address.line.extension[houseNumber])
* insert ObligationRules(address.line.extension[houseNumberLetter-houseNumberAddition])
* insert ObligationRules(address.line.extension[houseNumberIndication])
* insert ObligationRules(address.postalCode)
* insert ObligationRules(address.city)
* insert ObligationRules(address.district)
* insert ObligationRules(address.country.extension[countryCode])
* insert ObligationRules(address.line.extension[additionalInformation])
* insert ObligationRules(address.use)
* insert ObligationRules(address.type)

Mapping: MapACPPatient
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPPatient
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "351" "Patient"
* -> "613" "Patient"
* -> "648" "Patient"
* identifier -> "385" "Identificatienummer"
* name -> "352" "Naamgegevens"
* name[nameInformation].given -> "353" "Voornamen"
* name[nameInformation].given -> "354" "Initialen"
* name[nameInformation-GivenName].given -> "355" "Roepnaam"
* name[nameInformation].use -> "356" "Naamgebruik"
// 357 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix] -> "358" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "359" "Achternaam"
// 360 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix] -> "361" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName] -> "362" "AchternaamPartner"
* name[nameInformation].suffix -> "363" "Titels"
* name -> "515" "Naamgegevens"
* name[nameInformation].given -> "516" "Voornamen"
* name[nameInformation].given -> "517" "Initialen"
* name[nameInformation-GivenName].given -> "518" "Roepnaam"
* name[nameInformation].use -> "519" "Naamgebruik"
// 520 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix] -> "521" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "522" "Achternaam"
// 523 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix] -> "524" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName] -> "525" "AchternaamPartner"
* name[nameInformation].suffix -> "526" "Titels"
* telecom -> "376" "Contactgegevens" 
* telecom[telephoneNumbers] -> "377" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "378" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "379" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept -> "379" "TelecomType"
* telecom[telephoneNumbers].use -> "380" "NummerSoort"
* telecom[telephoneNumbers].extension[comment] -> "381" "Toelichting"
* telecom[emailAddresses] -> "382" "EmailAdressen"
* telecom[emailAddresses].value -> "383" "EmailAdres"
* telecom[emailAddresses].system -> "384" "EmailSoort"
* gender -> "387" "Geslacht"
* gender.extension[genderCodelist] -> "387" "Geslacht" 
* birthDate -> "386" "Geboortedatum"
* address -> "364" "Adresgegevens"
* address.line.extension[streetName] -> "365" "Straat"
* address.line.extension[houseNumber] -> "366" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "367" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "368" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication] -> "369" "AanduidingBijHuisnummer"
* address.postalCode -> "370" "Postcode"
* address.city -> "371" "Woonplaats"
* address.district -> "372" "Gemeente"
* address.country.extension[countryCode] -> "373" "Land"
* address.line.extension[additionalInformation] -> "374" "AdditioneleInformatie"
* address.use -> "375" "AdresSoort"
* address.type -> "375" "AdresSoort"


Instance: ACP-Patient-HendrikHartman-Pat1
InstanceOf: ACPPatient
Title: "ACP Patient - Hendrik Hartman - Pat 1"
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
* contact.extension[relatedPerson].valueReference = Reference(ACP-ContactPerson-MichielHartman-Pat1)
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


Instance: ACP-Patient-SamiraVanDerSluijs-Pat2
InstanceOf: ACPPatient
Title: "ACP Patient - Samira van der Sluijs - Pat 2"
Usage: #example
* identifier.system = "http://fhir.nl/fhir/NamingSystem/bsn"
* identifier.value = "999998298"
* name[0].use = #official
* name[=].text = "Samira van der Sluijs"
* name[=].family = "van der Sluijs"
* name[=].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[=].family.extension[=].valueString = "Sluijs"
* name[=].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name[=].family.extension[=].valueString = "van der"
* name[=].given[0] = "Samira"
* name[=].given[+] = "Louise"
* name[=].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #BR
* name[=].given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #BR
* name[+].use = #usual
* name[=].given = "Samira"
* telecom[+].system = #phone
* telecom[=].system.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[=].system.extension.valueCodeableConcept = $v3-AddressUse#MC "mobile contact"
* telecom[=].value = "0688877788"
* telecom[=].use = #home
* telecom[+].system = #email
* telecom[=].value = "samira.test@iknl.nl"
* telecom[=].use = #work
* gender = #female
* gender.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* gender.extension.valueCodeableConcept = $v3-AdministrativeGender#F "Female"
* birthDate = "1959-07-31"
* address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address.extension.valueCodeableConcept = $v3-AddressUse#HP "Primary Home"
* address.use = #home
* address.type = #both
* address.line = "Vasteland 78"
* address.line.extension[0].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"
* address.line.extension[=].valueString = "Vasteland"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"
* address.line.extension[=].valueString = "78"
* address.city = "Rotterdam"
* address.district = "Rotterdam"
* address.postalCode = "3011BN"
* address.country = "Nederland"
* address.country.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* address.country.extension.valueCodeableConcept.coding = urn:iso:std:iso:3166#NL "Netherlands"
* contact[0].name.text = "Gert-Jan de Jong"
* contact[0].name.use = #official
* contact[0].extension[relatedPerson].valueReference = Reference(ACP-ContactPerson-GertJanDeJong-Pat2)
* contact[+].name.text = "Maya van der Sluijs-Mulder"
* contact[+].name.use = #official
* contact[+].extension[relatedPerson].valueReference = Reference(ACP-ContactPerson-MayaVanDerSluijsMulder-Pat2)

Profile: ACPContactPerson
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-ContactPerson
Id: ACP-ContactPerson
Title: "ContactPerson"
Description: "A person not being a healthcare professional who is involved in the patient’s care, such as family members, caregivers, mental caretakers, guardians and legal representatives. Based on nl-core-ContactPerson and HCIM ContactPerson."
* insert MetaRules
* patient only Reference(ACPPatient)
* relationship 1..*
* relationship[role] 1..* 
* relationship[relationship] ^definition = "When someone is or **will be** a legal representative, then a relationship code `24` from code system  _urn:oid:2.16.840.1.113883.2.4.3.11.22.472_ is added."


Mapping: MapACPContactPerson
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPContactPerson
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "441" "Wettelijk vertegenwoordiger (Contactpersoon)"
* -> "615" "Contactpersoon"
* -> "650" "Contactpersoon"
* -> "696" "Contactpersoon"
* -> "706" "Contactpersoon"
* -> "727" "Contactpersoon"
* name -> "442" "Naamgegevens"
* name[nameInformation].given -> "443" "Voornamen"
* name[nameInformation].given -> "444" "Initialen"
* name[nameInformation-GivenName].given -> "445" "Roepnaam"
* name[nameInformation].use -> "446" "Naamgebruik"
// 447 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix].valueString -> "448" "Voorvoegsels"
* name[nameInformation].family.extension[lastName].valueString -> "449" "Achternaam"
// 450 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix].valueString -> "451" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName].valueString -> "452" "AchternaamPartner"
* name[nameInformation].suffix -> "453" "Titels"
* telecom -> "454" "Contactgegevens"
* telecom[telephoneNumbers] -> "455" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "456" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "457" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept -> "457" "TelecomType"
* telecom[telephoneNumbers].use -> "458" "NummerSoort"
* telecom[telephoneNumbers].extension[comment].valueString -> "459" "Toelichting"
* telecom[emailAddresses] -> "460" "EmailAdressen"
* telecom[emailAddresses].value -> "461" "EmailAdres"
* telecom[emailAddresses].system -> "462" "EmailSoort"
* address -> "463" "Adresgegevens"
* address.line.extension[streetName].valueString -> "464" "Straat"
* address.line.extension[houseNumber].valueString -> "465" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "466" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "467" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication].valueString -> "468" "AanduidingBijHuisnummer"
* address.postalCode -> "469" "Postcode"
* address.city -> "470" "Woonplaats"
* address.district -> "471" "Gemeente"
* address.country.extension[countryCode].valueCodeableConcept -> "472" "Land"
* address.line.extension[additionalInformation].valueString -> "473" "AdditioneleInformatie"
* address.use -> "474" "AdresSoort"
* address.type -> "474" "AdresSoort"
* relationship[role] -> "475" "Rol"
* relationship[role] -> "477" "Vertegenwoordiger is contactpersoon"
* relationship[relationship] -> "476" "Relatie"
* -> "478" "Eerste contactpersoon (Contactpersoon)" 
* name -> "479" "Naamgegevens"
* name[nameInformation].given -> "480" "Voornamen"
* name[nameInformation].given -> "481" "Initialen"
* name[nameInformation-GivenName].given -> "482" "Roepnaam"
* name[nameInformation].use -> "483" "Naamgebruik"
// 484 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix].valueString -> "485" "Voorvoegsels"
* name[nameInformation].family.extension[lastName].valueString -> "486" "Achternaam"
// 487 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix].valueString -> "488" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName].valueString -> "489" "AchternaamPartner"
* name[nameInformation].suffix -> "490" "Titels"
* telecom -> "491" "Contactgegevens"
* telecom[telephoneNumbers] -> "492" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "493" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "494" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept -> "494" "TelecomType"
* telecom[telephoneNumbers].use -> "495" "NummerSoort"
* telecom[telephoneNumbers].extension[comment].valueString -> "496" "Toelichting"
* telecom[emailAddresses] -> "497" "EmailAdressen"
* telecom[emailAddresses].value -> "498" "EmailAdres"
* telecom[emailAddresses].system -> "499" "EmailSoort"
* address -> "500" "Adresgegevens" 
* address.line.extension[streetName].valueString -> "501" "Straat"
* address.line.extension[houseNumber].valueString -> "502" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "503" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition].valueString -> "504" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication].valueString -> "505" "AanduidingBijHuisnummer"
* address.postalCode -> "506" "Postcode"
* address.city -> "507" "Woonplaats"
* address.district -> "508" "Gemeente"
* address.country.extension[countryCode].valueCodeableConcept -> "509" "Land"
* address.line.extension[additionalInformation].valueString -> "510" "AdditioneleInformatie"
* address.use -> "511" "AdresSoort"
* address.type -> "511" "AdresSoort"
* relationship[role] -> "512" "Rol"
* relationship[relationship] -> "513" "Relatie"
* -> "554" "Gesprek gevoerd in bijzijn van (Contactpersoon)" 
* name -> "555" "Naamgegevens"
* name[nameInformation].given -> "556" "Voornamen"
* name[nameInformation].given -> "557" "Initialen"
* name[nameInformation-GivenName].given -> "558" "Roepnaam"
* name[nameInformation].use -> "559" "Naamgebruik"
// 560 - Geslachtsnaam - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[prefix].valueString -> "561" "Voorvoegsels"
* name[nameInformation].family.extension[lastName].valueString -> "562" "Achternaam"
// 563 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix].valueString -> "564" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName].valueString -> "565" "AchternaamPartner"
* name[nameInformation].suffix -> "566" "Titels"
* relationship[role] -> "588" "Rol"
* relationship[relationship] -> "589" "Relatie"


Instance: F1-ACP-ContactPerson-MichielHartman
InstanceOf: ACPContactPerson
Title: "F1 ACP ContactPerson Michiel Hartman"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ebe579d0-fda9-4440-ac6c-6afb0b338006"
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* relationship[+] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24 "Wettelijke vertegenwoordiger"
* relationship[+] = $v3-RoleCode#BRO "brother"
* name[0].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[=].extension.valueCode = #NL1
* name[=].use = #official
* name[=].text = "Michiel Hartman"
* name[=].family = "Hartman"
* name[=].family.extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[=].family.extension.valueString = "Hartman"
* name[=].given[0] = "Michiel"
* name[=].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #BR
* name[+].use = #usual
* name[=].given = "Michiel"
* telecom[0].system = #email
* telecom[=].value = "michiel.hartman@iknl.nl"
* telecom[=].use = #work
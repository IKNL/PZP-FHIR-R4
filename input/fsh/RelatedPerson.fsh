
Profile: ACPContactPerson
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-ContactPerson
Id: ACP-ContactPerson
Title: "ACP ContactPerson"
Description: "A person not being a healthcare professional who is involved in the patient’s care, such as family members, caregivers, mental caretakers, guardians and legal representatives. Based on nl-core-ContactPerson and HCIM ContactPerson."
* insert MetaRules
* obeys ACP-ContactPerson-1
* patient only Reference(ACPPatient)
* relationship contains
    roleAdditional 0..*
* relationship ^short = "At least one relationship element SHALL be provided with a role code from either the role or roleAdditional slice. The roleAdditional slice contains additional codes introduced in the zib2024 release."
* relationship[role] ^comment = "For the ACP use case, additional codes beyond those in the existing ContactPerson [RolCodelijst](http://decor.nictiz.nl/fhir/ValueSet/2.16.840.1.113883.2.4.3.11.60.40.2.3.1.2--20200901000000) are required. This is permitted by the zib's extensible binding. However, the ValueSet is bound as 'required' in this slice to ensure the slicing works correctly. Therefore, an additional slice has been added containing a bound ValueSet with the extra codes."
* relationship[roleAdditional] from ACPContactPersonRoleVS (required)
* relationship[roleAdditional] ^comment = "This slice contains codes not included in the RolCodelijst that is bound to the role slice."
* relationship[relationship] ^definition = "When someone is or **will be** a legal representative, then a relationship code `24` from code system  _urn:oid:2.16.840.1.113883.2.4.3.11.22.472_ is added."

* insert ObligationRules(patient)
* insert ObligationRules(relationship[role])
* insert ObligationRules(relationship[roleAdditional])
* insert ObligationRules(relationship[relationship])
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

Invariant: ACP-ContactPerson-1
Description: "At least one relationship element must contain a role code from the role slice (RolCodelijst) or the roleAdditional slice (ACPContactPersonRoleVS)."
Severity: #error
Expression: "relationship.coding.where((system = 'urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4.23.1' and (code = '100001' or code = '100002' or code = '100003' or code = '100004')) or (system = 'urn:oid:2.16.840.1.113883.2.4.3.11.22.472' and (code = '01' or code = '02' or code = '03' or code = '04' or code = '05' or code = '06' or code = '07' or code = '09' or code = '11' or code = '14' or code = '15' or code = '19' or code = '20' or code = '21' or code = '23' or code = '24')) or (system = 'http://snomed.info/sct' and code = '310141000146103')).exists()"

Mapping: MapACPContactPerson
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPContactPerson
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
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
* name[nameInformation].family.extension[prefix] -> "448" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "449" "Achternaam"
// 450 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix] -> "451" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName] -> "452" "AchternaamPartner"
* name[nameInformation].suffix -> "453" "Titels"
* telecom -> "454" "Contactgegevens"
* telecom[telephoneNumbers] -> "455" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "456" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "457" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType] -> "457" "TelecomType"
* telecom[telephoneNumbers].use -> "458" "NummerSoort"
* telecom[telephoneNumbers].extension[comment] -> "459" "Toelichting"
* telecom[emailAddresses] -> "460" "EmailAdressen"
* telecom[emailAddresses].value -> "461" "EmailAdres"
* telecom[emailAddresses].system -> "462" "EmailSoort"
* address -> "463" "Adresgegevens"
* address.line.extension[streetName] -> "464" "Straat"
* address.line.extension[houseNumber] -> "465" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "466" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "467" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication] -> "468" "AanduidingBijHuisnummer"
* address.postalCode -> "469" "Postcode"
* address.city -> "470" "Woonplaats"
* address.district -> "471" "Gemeente"
* address.country.extension[countryCode] -> "472" "Land"
* address.line.extension[additionalInformation] -> "473" "AdditioneleInformatie"
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
* name[nameInformation].family.extension[prefix] -> "485" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "486" "Achternaam"
// 487 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix] -> "488" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName] -> "489" "AchternaamPartner"
* name[nameInformation].suffix -> "490" "Titels"
* telecom -> "491" "Contactgegevens"
* telecom[telephoneNumbers] -> "492" "Telefoonnummers"
* telecom[telephoneNumbers].value -> "493" "Telefoonnummer"
* telecom[telephoneNumbers].system -> "494" "TelecomType"
* telecom[telephoneNumbers].system.extension[telecomType] -> "494" "TelecomType"
* telecom[telephoneNumbers].use -> "495" "NummerSoort"
* telecom[telephoneNumbers].extension[comment] -> "496" "Toelichting"
* telecom[emailAddresses] -> "497" "EmailAdressen"
* telecom[emailAddresses].value -> "498" "EmailAdres"
* telecom[emailAddresses].system -> "499" "EmailSoort"
* address -> "500" "Adresgegevens" 
* address.line.extension[streetName] -> "501" "Straat"
* address.line.extension[houseNumber] -> "502" "Huisnummer"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "503" "Huisnummerletter"
* address.line.extension[houseNumberLetter-houseNumberAddition] -> "504" "Huisnummertoevoeging"
* address.line.extension[houseNumberIndication] -> "505" "AanduidingBijHuisnummer"
* address.postalCode -> "506" "Postcode"
* address.city -> "507" "Woonplaats"
* address.district -> "508" "Gemeente"
* address.country.extension[countryCode] -> "509" "Land"
* address.line.extension[additionalInformation] -> "510" "AdditioneleInformatie"
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
* name[nameInformation].family.extension[prefix] -> "561" "Voorvoegsels"
* name[nameInformation].family.extension[lastName] -> "562" "Achternaam"
// 563 - GeslachtsnaamPartner - is not mapped as there is no element for this container. It is also not mapped in the zib profile.
* name[nameInformation].family.extension[partnerPrefix] -> "564" "VoorvoegselsPartner"
* name[nameInformation].family.extension[partnerLastName] -> "565" "AchternaamPartner"
* name[nameInformation].suffix -> "566" "Titels"
* relationship[role] -> "588" "Rol"
* relationship[relationship] -> "589" "Relatie"


Instance: ACP-ContactPerson-MichielHartman-Pat1
InstanceOf: ACPContactPerson
Title: "ACP ContactPerson - Michiel Hartman - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ebe579d0-fda9-4440-ac6c-6afb0b338006"
* patient = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
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


Instance: ACP-ContactPerson-GertJanDeJong-Pat2
InstanceOf: ACPContactPerson
Title: "ACP ContactPerson Gert-Jan de Jong - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "944f2f14-ccec-47cb-a90f-d2401332a316"
* patient = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24 "Wettelijke vertegenwoordiger"
* relationship[+] = $v3-RoleCode#HUSB "husband"
* name.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name.extension[=].valueCode = #NL1
* name.use = #official
* name.text = "Gert-Jan de Jong"
* name.family = "de Jong"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name.family.extension[=].valueString = "de"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension[=].valueString = "Jong"
* name.given[0] = "Gert-Jan"
* name.given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name.given[=].extension.valueCode = #BR
* telecom[0].system = #phone
* telecom[=].system.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[=].system.extension.valueCodeableConcept = $v3-AddressUse#MC "mobile contact"
* telecom[=].value = "0611111111"
* telecom[=].use = #home
* telecom[+].system = #email
* telecom[=].value = "Gert-Jan@test.nl"
* telecom[=].use = #home
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


Instance: ACP-ContactPerson-MayaVanDerSluijsMulder-Pat2
InstanceOf: ACPContactPerson
Title: "ACP ContactPerson - Maya van der Sluijs-Mulder - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "833d8550-2e63-4c31-a210-20eaeb1d43da"
* patient = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#23 "contactpersoon"
* relationship[+] = $v3-RoleCode#SIS "sister"
* name.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name.extension[=].valueCode = #NL4
* name.use = #official
* name.text = "Maya van der Sluijs-Mulder"
* name.family = "van der Sluijs-Mulder"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name.family.extension[=].valueString = "van der"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name.family.extension[=].valueString = "Sluijs"
* name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* name.family.extension[=].valueString = "Mulder"
* name.given[0] = "Maya"
* name.given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name.given[=].extension.valueCode = #BR
* telecom[0].system = #phone
* telecom[=].system.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[=].system.extension.valueCodeableConcept = $v3-AddressUse#MC "mobile contact"
* telecom[=].value = "0622222222"
* telecom[=].use = #home
* telecom[+].system = #email
* telecom[=].value = "maya@test.nl"
* telecom[=].use = #home
* address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address.extension.valueCodeableConcept = $v3-AddressUse#HP "Primary Home"
* address.use = #home
* address.type = #both
* address.line = "Spoorsingel 41B"
* address.line.extension[0].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"
* address.line.extension[=].valueString = "Spoorsingel"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"
* address.line.extension[=].valueString = "41"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* address.line.extension[=].valueString = "B"
* address.city = "Delft"
* address.district = "Delft"
* address.postalCode = "2613BG"
* address.country = "Nederland"
* address.country.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* address.country.extension.valueCodeableConcept.coding = urn:iso:std:iso:3166#NL "Netherlands"
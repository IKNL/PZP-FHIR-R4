
Instance: P1-ACP-ContactPerson-HendrikHartman
InstanceOf: ACPContactPerson
Title: "P1 ACP ContactPerson Hendrik Hartman"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "6504c755-8466-4647-9e53-d6b51d459f3e"
* patient = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#24 "Wettelijke vertegenwoordiger"
* relationship[+] = $v3-RoleCode#BRO "Brother"
* name[0].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[=].extension.valueCode = #NL1
* name[=].use = #official
* name[=].text = "Michiel Hartman"
* name[=].family = "Hartman"
* name[=].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[=].family.extension[=].valueString = "Hartman"
* name[=].given[0] = "M"
* name[=].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #IN // not sure if I should also include initials
* name[=].given[1] = "Michiel"
* name[=].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[=].given[=].extension.valueCode = #BR
* name[+].use = #usual
* name[=].given = "Michiel"
* telecom[0].system = #phone
* telecom[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[0].extension[0].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressUse"
* telecom[0].extension[0].valueCodeableConcept.coding[0].code = #MC
* telecom[0].extension[0].valueCodeableConcept.coding[0].display = "Mobile Phone"
* telecom[=].value = "06-45612378"
* telecom[0].use = #home
* telecom[1].system = #email
* telecom[=].value = "michiel@test.nl"
* telecom[=].use = #home
* address[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address[0].extension[0].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressType"
* address[0].extension[0].valueCodeableConcept.coding[0].code = #HP
* address[0].extension[0].valueCodeableConcept.coding[0].display = "Primary Home"
* address[0].use = #home
* address[0].type = #both
* address[0].line = "Keizersgracht 764A IV"
* address[0].line[0].extension[0].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-streetName"
* address[0].line[0].extension[=].valueString = "Keizersgracht"
* address[0].line[0].extension[1].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-houseNumber"
* address[0].line[0].extension[=].valueString = "764"
* address[0].line[0].extension[2].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* address[0].line[0].extension[=].valueString = "A"
* address[0].line[0].extension[3].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-additionalLocator"
* address[0].line[0].extension[=].valueString = "IV"
* address[0].city = "Amsterdam"
* address[0].district = "Amsterdam"
* address[0].postalCode = "1017 EZ"
* address[0].country = "Nederland"
* address[0].country.extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* address[0].country.extension[=].valueCodeableConcept.coding[0].system = "urn:iso:std:iso:3166"
* address[0].country.extension[=].valueCodeableConcept.coding[0].version = "2020-10-26T00:00:00"
* address[0].country.extension[=].valueCodeableConcept.coding[0].code = #NL
* address[0].country.extension[=].valueCodeableConcept.coding[0].display = "Netherlands"

Instance: P1-ACP-ContactPerson1-HendrikHartman
InstanceOf: ACPContactPerson
Title: "P1 ACP ContactPerson1 Hendrik Hartman"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "2ee35302-cd40-40d5-b7b4-15f103662c7b"
* patient = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* patient.type = "Patient"
* relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* relationship[+] = $v3-RoleCode#WIFE "Wife"
* name[nameInformation].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[nameInformation].extension.valueCode = #NL4
* name[nameInformation].use = #official
* name[nameInformation].text = "Mirjam de Leeuw Hartman"
* name[nameInformation].family = "de Leeuw"
* name[nameInformation].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name[nameInformation].family.extension[prefix].valueString = "de"
* name[nameInformation].family.extension[1].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[nameInformation].family.extension[lastName].valueString = "Leeuw"
* name[nameInformation].family.extension[2].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* name[nameInformation].family.extension[partnerLastName].valueString = "Hartman"
* name[nameInformation].given[0] = "M"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #IN
* name[nameInformation].given[1] = "Mirjam"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation-GivenName].use = #usual
* name[nameInformation-GivenName].given = "Mirjam"
* telecom[0].system = #phone
* telecom[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[0].extension[0].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressUse"
* telecom[0].extension[0].valueCodeableConcept.coding[0].code = #MC
* telecom[0].extension[0].valueCodeableConcept.coding[0].display = "Mobile Phone"
* telecom[=].value = "06-98765432"
* telecom[0].use = #home
* telecom[1].system = #email
* telecom[=].value = "mirjam@test.nl"
* telecom[=].use = #home
* address[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address[=].extension[=].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressType"
* address[=].extension[=].valueCodeableConcept.coding[=].code = #HP
* address[=].extension[=].valueCodeableConcept.coding[=].display = "Primary Home"
* address[=].use = #home
* address[=].type = #both
* address[=].line = "Twijnstraat 24A BIS"
* address[=].line[0].extension[0].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-streetName"
* address[=].line[=].extension[=].valueString = "Twijnstraat"
* address[=].line[=].extension[1].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-houseNumber"
* address[=].line[=].extension[=].valueString = "24"
* address[=].line[=].extension[2].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* address[=].line[=].extension[=].valueString = "A"
* address[=].line[=].extension[3].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-additionalLocator"
* address[=].line[=].extension[=].valueString = "BIS"
* address[=].city = "Utrecht"
* address[=].district = "Utrecht"
* address[=].postalCode = "3511 ZL"
* address[=].country = "Nederland"
* address[=].country.extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* address[=].country.extension[=].valueCodeableConcept.coding[0].system = "urn:iso:std:iso:3166"
* address[=].country.extension[=].valueCodeableConcept.coding[=].version = "2020-10-26T00:00:00"
* address[=].country.extension[=].valueCodeableConcept.coding[=].code = #NL
* address[=].country.extension[=].valueCodeableConcept.coding[=].display = "Netherlands"
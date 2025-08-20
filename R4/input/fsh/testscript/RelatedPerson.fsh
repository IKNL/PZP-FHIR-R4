Instance: P2-ACP-ContactPerson-GertJanDeJong
InstanceOf: ACP-ContactPerson
Title: "P2 ACP ContactPerson Gert-Jan de Jong"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "944f2f14-ccec-47cb-a90f-d2401332a316"
* patient = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
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
* telecom[telephoneNumbers].system = #phone
* telecom[telephoneNumbers].system.extension[+].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[telephoneNumbers].system.extension[=].valueCode = #MC
* telecom[telephoneNumbers].value = "0611111111"
* telecom[telephoneNumbers].use = #home
* telecom[emailAddresses].system = #email
* telecom[emailAddresses].value = "Gert-Jan@test.nl"
* telecom[emailAddresses].use = #home 
* address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address.extension.valueCodeableConcept = #HP
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
* address.country.extension.valueCodeableConcept.coding.version = "2020-10-26T00:00:00"
* address.country.extension.valueCodeableConcept.coding = urn:iso:std:iso:3166#NL "Nederland"

Instance: P2-ACP-ContactPerson-MayaVanDerSluijsMulder
InstanceOf: ACP-ContactPerson
Title: "P2 ACP ContactPerson Maya van der Sluijs-Mulder"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "833d8550-2e63-4c31-a210-20eaeb1d43da"
* patient = Reference(P2-ACP-Patient-SamiraVanDerSluijs) "Patient, Samira van der Sluijs"
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
* telecom[telephoneNumbers].system = #phone
* telecom[telephoneNumbers].system.extension[+].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[telephoneNumbers].system.extension[=].valueCode = #MC
* telecom[telephoneNumbers].value = "0622222222"
* telecom[telephoneNumbers].use = #home
* telecom[emailAddresses].system = #email
* telecom[emailAddresses].value = "maya@test.nl"
* telecom[emailAddresses].use = #home
* address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address.extension.valueCodeableConcept = #HP
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
* address.country.extension.valueCodeableConcept.coding.version = "2020-10-26T00:00:00"
* address.country.extension.valueCodeableConcept.coding = urn:iso:std:iso:3166#NL "Nederland"
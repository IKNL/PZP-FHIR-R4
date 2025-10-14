Instance: P1-ACP-Patient-HendrikHartman
InstanceOf: ACPPatient
Title: "P1 ACP Patient Hendrik Hartman"
Usage: #example
* extension[legallyCapableMedicalTreatmentDecisions].extension[legallyCapable].valueBoolean = false
* identifier.system = "http://fhir.nl/fhir/NamingSystem/bsn"
* identifier.value = "999998286"
* name[nameInformation].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* name[nameInformation].extension.valueCode = #NL4
* name[nameInformation].use = #official
* name[nameInformation].text = "Hendrik Hartman de Leeuw"
* name[nameInformation].family = "Hartman"
* name[nameInformation].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[nameInformation].family.extension[=].valueString = "Hartman"
* name[nameInformation].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-prefix"
* name[nameInformation].family.extension[=].valueString = "de"
* name[nameInformation].family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* name[nameInformation].family.extension[=].valueString = "Leeuw"
* name[nameInformation].given[0] = "H"
* name[nameInformation].given[+] = "J"
* name[nameInformation].given[+] = "Hendrik"
* name[nameInformation].given[+] = "Johan"
* name[nameInformation].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #IN
* name[nameInformation].given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #IN
* name[nameInformation].given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation].given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation-GivenName].use = #usual
* name[nameInformation-GivenName].given = "Rik"
* telecom[0].system = #phone
* telecom[=].system.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[=].system.extension.valueCodeableConcept = $v3-AddressUse#MC "mobile contact"
* telecom[=].value = "06-00112233"
* telecom[=].use = #home
* telecom[+].system = #email
* telecom[=].value = "test@iknl.nl"
* telecom[=].use = #work
* gender = #male
* gender.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* gender.extension.valueCodeableConcept = $v3-AdministrativeGender#M "Male"
* birthDate = "1961-03-21"
* address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* address.extension.valueCodeableConcept = $v3-AddressUse#HP "Primary Home"
* address.use = #home
* address.type = #both
* address.line = "Twijnstraat 24A BIS"
* address.line.extension[0].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"
* address.line.extension[=].valueString = "Twijnstraat"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"
* address.line.extension[=].valueString = "24"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* address.line.extension[=].valueString = "A"
* address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-unitID"
* address.line.extension[=].valueString = "BIS"
* address.city = "Utrecht"
* address.district = "Utrecht"
* address.postalCode = "3511 ZL"
* address.country = "Nederland"
* address.country.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* address.country.extension.valueCodeableConcept.coding.version = "2020-10-26T00:00:00"
* address.country.extension.valueCodeableConcept.coding = urn:iso:std:iso:3166#NL "Netherlands"
* contact.extension[relatedPerson].valueReference = Reference(P1-ACP-ContactPerson-MirjamDeLeeuwHartman)
* contact.relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* contact.relationship[+] = $v3-RoleCode#WIFE "Wife"
* contact.name.extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* contact.name.extension.valueCode = #NL4
* contact.name.use = #official
* contact.name.text = "Mirjam de Leeuw Hartman"
* contact.name.family = "de Leeuw"
* contact.name.family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* contact.name.family.extension[=].valueString = "de"
* contact.name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* contact.name.family.extension[=].valueString = "Leeuw"
* contact.name.family.extension[+].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* contact.name.family.extension[=].valueString = "Hartman"
* contact.name.given[0] = "M"
* contact.name.given[+] = "Mirjam"
* contact.name.given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* contact.name.given[=].extension.valueCode = #IN
* contact.name.given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* contact.name.given[=].extension.valueCode = #BR
* contact.telecom[0].system = #phone
* contact.telecom[=].system.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* contact.telecom[=].system.extension.valueCodeableConcept = $v3-AddressUse#MC "mobile contact"
* contact.telecom[=].value = "06-98765432"
* contact.telecom[=].use = #home
* contact.telecom[+].system = #email
* contact.telecom[=].value = "mirjam@test.nl"
* contact.telecom[=].use = #home
* contact.address.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* contact.address.extension.valueCodeableConcept = $v3-AddressUse#HP "Primary Home"
* contact.address.use = #home
* contact.address.type = #both
* contact.address.line = "Twijnstraat 24A BIS"
* contact.address.line.extension[0].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-streetName"
* contact.address.line.extension[=].valueString = "Twijnstraat"
* contact.address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-houseNumber"
* contact.address.line.extension[=].valueString = "24"
* contact.address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* contact.address.line.extension[=].valueString = "A"
* contact.address.line.extension[+].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-unitID"
* contact.address.line.extension[=].valueString = "BIS"
* contact.address.city = "Utrecht"
* contact.address.district = "Utrecht"
* contact.address.postalCode = "3511 ZL"
* contact.address.country = "Nederland"
* contact.address.country.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* contact.address.country.extension.valueCodeableConcept.coding.version = "2020-04-01T00:00:00"
* contact.address.country.extension.valueCodeableConcept.coding = urn:oid:2.16.840.1.113883.2.4.4.16.34#6030 "Netherlands"

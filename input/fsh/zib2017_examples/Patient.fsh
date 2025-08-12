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
* name[nameInformation].family.extension[lastName].valueString = "Hartman"
* name[nameInformation].family.extension[1].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-prefix"
* name[nameInformation].family.extension[partnerPrefix].valueString = "de"
* name[nameInformation].family.extension[2].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* name[nameInformation].family.extension[partnerLastName].valueString = "Leeuw"
* name[nameInformation].given[0] = "H"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #IN
* name[nameInformation].given[1] = "J"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #IN
* name[nameInformation].given[2] = "Hendrik"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation].given[3] = "Johan"
* name[nameInformation].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation-GivenName].use = #usual
* name[nameInformation-GivenName].given = "Rik"
* telecom[0].system = #phone
* telecom[=].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[=].extension[=].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressUse"
* telecom[=].extension[=].valueCodeableConcept.coding[=].code = #MC
* telecom[=].extension[=].valueCodeableConcept.coding[=].display = "Mobile Phone"
* telecom[=].value = "06-00112233"
* telecom[=].use = #home
* telecom[1].system = #email
* telecom[=].value = "test@iknl.nl"
* telecom[=].use = #work
* gender = #male
* gender.extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* gender.extension[=].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AdministrativeGender"
* gender.extension[=].valueCodeableConcept.coding[=].code = #M
* gender.extension[=].valueCodeableConcept.coding[=].display = "Male"
* birthDate = "1961-03-21"
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
* contact.extension[relatedPerson].valueReference = Reference(P1-ACP-ContactPerson1-HendrikHartman)
* contact.relationship[0] = urn:oid:2.16.840.1.113883.2.4.3.11.22.472#01 "Eerste relatie/contactpersoon"
* contact.relationship[+] = $v3-RoleCode#WIFE "Wife"
* contact.name[0].extension.url = "http://hl7.org/fhir/StructureDefinition/humanname-assembly-order"
* contact.name[=].extension.valueCode = #NL4
* contact.name[=].use = #official
* contact.name[=].text = "Mirjam de Leeuw Hartman"
* contact.name[=].family = "de Leeuw"
* contact.name[=].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* contact.name[=].family.extension[prefix].valueString = "de"
* contact.name[=].family.extension[1].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* contact.name[=].family.extension[lastName].valueString = "Leeuw"
* contact.name[=].family.extension[2].url = "http://hl7.org/fhir/StructureDefinition/humanname-partner-name"
* contact.name[=].family.extension[partnerLastName].valueString = "Hartman"
* contact.name[=].given[0] = "M"
* contact.name[=].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* contact.name[=].given[=].extension.valueCode = #IN
* contact.name[=].given[1] = "Mirjam"
* contact.name[=].given[=].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* contact.name[=].given[=].extension.valueCode = #BR
* contact.telecom[0].system = #phone
* contact.telecom[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* contact.telecom[0].extension[0].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressUse"
* contact.telecom[0].extension[0].valueCodeableConcept.coding[0].code = #MC
* contact.telecom[0].extension[0].valueCodeableConcept.coding[0].display = "Mobile Phone"
* contact.telecom[=].value = "06-98765432"
* contact.telecom[0].use = #home
* contact.telecom[1].system = #email
* contact.telecom[=].value = "mirjam@test.nl"
* contact.telecom[=].use = #home
* contact.address[0].extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-AddressInformation.AddressType"
* contact.address[0].extension[0].valueCodeableConcept.coding[0].system = "http://terminology.hl7.org/CodeSystem/v3-AddressType"
* contact.address[0].extension[0].valueCodeableConcept.coding[0].code = #HP
* contact.address[0].extension[0].valueCodeableConcept.coding[0].display = "Primary Home"
* contact.address[0].use = #home
* contact.address[0].type = #both
* contact.address[0].line = "Twijnstraat 24A BIS"
* contact.address[0].line[0].extension[0].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-streetName"
* contact.address[0].line[0].extension[=].valueString = "Twijnstraat"
* contact.address[0].line[0].extension[1].url = "http://hl7.org/fhir/StructureDefinition-iso21090-ADXP-houseNumber"
* contact.address[0].line[0].extension[=].valueString = "24"
* contact.address[0].line[0].extension[2].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-buildingNumberSuffix"
* contact.address[0].line[0].extension[=].valueString = "A"
* contact.address[0].line[0].extension[3].url = "http://hl7.org/fhir/StructureDefinition/iso21090-ADXP-additionalLocator"
* contact.address[0].line[0].extension[=].valueString = "BIS"
* contact.address[0].city = "Utrecht"
* contact.address[0].district = "Utrecht"
* contact.address[0].postalCode = "3511 ZL"
* contact.address[0].country = "Nederland"
* contact.address[0].country.extension[0].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* contact.address[0].country.extension[=].valueCodeableConcept.coding[0].system = "urn:iso:std:iso:3166"
* contact.address[0].country.extension[=].valueCodeableConcept.coding[0].version = "2020-10-26T00:00:00"
* contact.address[0].country.extension[=].valueCodeableConcept.coding[0].code = #NL
* contact.address[0].country.extension[=].valueCodeableConcept.coding[0].display = "Netherlands"

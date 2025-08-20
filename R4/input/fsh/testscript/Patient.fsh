Instance: P2-ACP-Patient-SamiraVanDerSluijs
InstanceOf: ACPPatient
Title: "P2 ACP Patient Samira van der Sluijs"
Usage: #example
* extension[legallyCapableMedicalTreatmentDecisions].extension[legallyCapable].valueBoolean = true
* extension[legallyCapableMedicalTreatmentDecisions].extension[legallyCapableComment].valueString = "Patiënt is wilsbekwaam. Bij verandering van de situatie wordt haar partner haar wettelijk vertegenwoordiger."
* identifier.system = "http://fhir.nl/fhir/NamingSystem/bsn"
* identifier.value = "999911121" // TODO toevoegen juiste bsn
* name[0].use = #official
* name[nameInformation].text = "Samira van der Sluijs"
* name[nameInformation].family = "van der Sluijs"
* name[nameInformation].family.extension[0].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-name"
* name[nameInformation].family.extension[=].valueString = "Sluijs"
* name[nameInformation].family.extension[1].url = "http://hl7.org/fhir/StructureDefinition/humanname-own-prefix"
* name[nameInformation].family.extension[=].valueString = "van der"
* name[nameInformation].given[0] = "Samira"
* name[nameInformation].given[+] = "Louise"
* name[nameInformation].given[0].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[nameInformation].given[+].extension.url = "http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier"
* name[nameInformation].given[=].extension.valueCode = #BR
* name[+].use = #usual
* name[=].given = "Samira"
* telecom[telephoneNumbers].system = #phone
* telecom[telephoneNumbers].system.extension[+].url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* telecom[telephoneNumbers].system.extension[=].valueCode = #MC
* telecom[telephoneNumbers].value = "0688877788"
* telecom[telephoneNumbers].use = #home
* telecom[emailAddresses].system = #email
* telecom[emailAddresses].value = "samira.test@iknl.nl"
* telecom[emailAddresses].use = #WP
* gender = #female
* gender.extension.url = "http://nictiz.nl/fhir/StructureDefinition/ext-CodeSpecification"
* gender.extension.valueCodeableConcept = #F "Female"
* birthDate = "1959-07-31"
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
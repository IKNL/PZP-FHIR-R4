#### Mappings by dataset ID

This table provides an overview of all dataset elements that are mapped to FHIR profiles in this implementation guide.

| ID | Dataset name | Resource | FHIR element |
|---|---|---|---|
| 736 | Datum van invullen | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `period.start`  |
| 351 | Patient | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | ``  |
| 352 | &emsp;Naamgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name`  |
| 353 | &emsp;&emsp;Voornamen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].given`  |
| 354 | &emsp;&emsp;Initialen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].given`  |
| 355 | &emsp;&emsp;Roepnaam | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation-GivenName].given`  |
| 356 | &emsp;&emsp;Naamgebruik | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].use`  |
| 358 | &emsp;&emsp;&emsp;Voorvoegsels | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[prefix].valueString`  |
| 359 | &emsp;&emsp;&emsp;Achternaam | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[lastName].valueString`  |
| 361 | &emsp;&emsp;&emsp;VoorvoegselsPartner | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[partnerPrefix].valueString`  |
| 362 | &emsp;&emsp;&emsp;AchternaamPartner | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[partnerLastName].valueString`  |
| 363 | &emsp;&emsp;Titels | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].suffix`  |
| 364 | &emsp;Adresgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address`  |
| 365 | &emsp;&emsp;Straat | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[streetName].valueString`  |
| 366 | &emsp;&emsp;Huisnummer | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[houseNumber].valueString`  |
| 367 | &emsp;&emsp;Huisnummerletter | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 368 | &emsp;&emsp;Huisnummertoevoeging | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 369 | &emsp;&emsp;AanduidingBijNummer | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[houseNumberIndication].valueString`  |
| 370 | &emsp;&emsp;Postcode | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.postalCode`  |
| 371 | &emsp;&emsp;Woonplaats | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.city`  |
| 372 | &emsp;&emsp;Gemeente | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.district`  |
| 373 | &emsp;&emsp;Land | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.country.extension[countryCode].valueCodeableConcept`  |
| 374 | &emsp;&emsp;AdditioneleInformatie | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.line.extension[additionalInformation].valueString`  |
| 375 | &emsp;&emsp;AdresSoort | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.use`  |
| 375 | &emsp;&emsp;AdresSoort | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address.type`  |
| 376 | &emsp;Contactgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom`  |
| 377 | &emsp;&emsp;Telefoonnummers | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers]`  |
| 378 | &emsp;&emsp;&emsp;Telefoonnummer | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers].value`  |
| 379 | &emsp;&emsp;&emsp;TelecomType | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers].system`  |
| 379 | &emsp;&emsp;&emsp;TelecomType | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept`  |
| 380 | &emsp;&emsp;&emsp;NummerSoort | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers].use`  |
| 381 | &emsp;&emsp;&emsp;Toelichting | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[telephoneNumbers].extension[comment].valueString`  |
| 382 | &emsp;&emsp;EmailAdressen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[emailAddresses]`  |
| 383 | &emsp;&emsp;&emsp;EmailAdres | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[emailAddresses].value`  |
| 384 | &emsp;&emsp;&emsp;EmailSoort | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom[emailAddresses].system`  |
| 385 | &emsp;Identificatienummer | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `identifier`  |
| 386 | &emsp;Geboortedatum | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `birthDate`  |
| 387 | &emsp;Geslacht | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `gender`  |
| 387 | &emsp;Geslacht | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `gender.extension[genderCodelist].value[x]`  |
| 391 | Gesprek gevoerd door (Zorgverlener) | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | ``  |
| 391 | Gesprek gevoerd door (Zorgverlener) | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | ``  |
| 392 | &emsp;ZorgverlenerIdentificatienummer | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `identifier`  |
| 393 | &emsp;Naamgegevens | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name`  |
| 394 | &emsp;&emsp;Voornamen | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation-GivenName].given`  |
| 398 | &emsp;&emsp;Geslachtsnaam | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family`  |
| 399 | &emsp;&emsp;&emsp;Voorvoegsels | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family.extension[prefix]`  |
| 400 | &emsp;&emsp;&emsp;Achternaam | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family.extension[lastName]`  |
| 405 | &emsp;Functie (Specialisme) | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | `specialty[specialty]`  |
| 761 | Wilsbekwaamheid m.b.t. medische behandelbeslissingen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `extension[legallyCapableMedicalTreatmentDecisions]`  |
| 762 | &emsp;Wilsbekwaamheid m.b.t. medische behandelbeslissingen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `extension[legallyCapableMedicalTreatmentDecisions].extension[legallyCapable].valueBoolean`  |
| 763 | &emsp;Toelichting | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `extension[legallyCapableMedicalTreatmentDecisions].extension[legallyCapableComment].valueString`  |
| 441 | Wettelijk vertegenwoordiger (Contactpersoon) | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 442 | &emsp;Naamgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name`  |
| 443 | &emsp;&emsp;Voornamen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 444 | &emsp;&emsp;Initialen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 445 | &emsp;&emsp;Roepnaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation-GivenName].given`  |
| 446 | &emsp;&emsp;Naamgebruik | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].use`  |
| 448 | &emsp;&emsp;&emsp;Voorvoegsels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[prefix].valueString`  |
| 449 | &emsp;&emsp;&emsp;Achternaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[lastName].valueString`  |
| 451 | &emsp;&emsp;&emsp;VoorvoegselsPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerPrefix].valueString`  |
| 452 | &emsp;&emsp;&emsp;AchternaamPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerLastName].valueString`  |
| 453 | &emsp;&emsp;Titels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].suffix`  |
| 454 | &emsp;Contactgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom`  |
| 455 | &emsp;&emsp;Telefoonnummers | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers]`  |
| 456 | &emsp;&emsp;&emsp;Telefoonnummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].value`  |
| 457 | &emsp;&emsp;&emsp;TelecomType | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].system`  |
| 457 | &emsp;&emsp;&emsp;TelecomType | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept`  |
| 458 | &emsp;&emsp;&emsp;NummerSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].use`  |
| 459 | &emsp;&emsp;&emsp;Toelichting | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].extension[comment].valueString`  |
| 460 | &emsp;&emsp;EmailAdressen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses]`  |
| 461 | &emsp;&emsp;&emsp;EmailAdres | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses].value`  |
| 462 | &emsp;&emsp;&emsp;EmailSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses].system`  |
| 463 | &emsp;Adresgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address`  |
| 464 | &emsp;&emsp;Straat | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[streetName].valueString`  |
| 465 | &emsp;&emsp;Huisnummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumber].valueString`  |
| 466 | &emsp;&emsp;Huisnummerletter | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 467 | &emsp;&emsp;Huisnummertoevoeging | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 468 | &emsp;&emsp;AanduidingBijNummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberIndication].valueString`  |
| 469 | &emsp;&emsp;Postcode | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.postalCode`  |
| 470 | &emsp;&emsp;Woonplaats | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.city`  |
| 471 | &emsp;&emsp;Gemeente | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.district`  |
| 472 | &emsp;&emsp;Land | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.country.extension[countryCode].valueCodeableConcept`  |
| 473 | &emsp;&emsp;AdditioneleInformatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[additionalInformation].valueString`  |
| 474 | &emsp;&emsp;AdresSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.use`  |
| 474 | &emsp;&emsp;AdresSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.type`  |
| 475 | &emsp;Rol | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[role]`  |
| 476 | &emsp;Relatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[relationship]`  |
| 477 | Vertegenwoordiger is contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[role]`  |
| 478 | Eerste contactpersoon (Contactpersoon) | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 479 | &emsp;Naamgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name`  |
| 480 | &emsp;&emsp;Voornamen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 481 | &emsp;&emsp;Initialen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 482 | &emsp;&emsp;Roepnaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation-GivenName].given`  |
| 483 | &emsp;&emsp;Naamgebruik | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].use`  |
| 485 | &emsp;&emsp;&emsp;Voorvoegsels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[prefix].valueString`  |
| 486 | &emsp;&emsp;&emsp;Achternaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[lastName].valueString`  |
| 488 | &emsp;&emsp;&emsp;VoorvoegselsPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerPrefix].valueString`  |
| 489 | &emsp;&emsp;&emsp;AchternaamPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerLastName].valueString`  |
| 490 | &emsp;&emsp;Titels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].suffix`  |
| 491 | &emsp;Contactgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom`  |
| 492 | &emsp;&emsp;Telefoonnummers | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers]`  |
| 493 | &emsp;&emsp;&emsp;Telefoonnummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].value`  |
| 494 | &emsp;&emsp;&emsp;TelecomType | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].system`  |
| 494 | &emsp;&emsp;&emsp;TelecomType | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].system.extension[telecomType].valueCodeableConcept`  |
| 495 | &emsp;&emsp;&emsp;NummerSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].use`  |
| 496 | &emsp;&emsp;&emsp;Toelichting | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[telephoneNumbers].extension[comment].valueString`  |
| 497 | &emsp;&emsp;EmailAdressen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses]`  |
| 498 | &emsp;&emsp;&emsp;EmailAdres | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses].value`  |
| 499 | &emsp;&emsp;&emsp;EmailSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom[emailAddresses].system`  |
| 500 | &emsp;Adresgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address`  |
| 501 | &emsp;&emsp;Straat | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[streetName].valueString`  |
| 502 | &emsp;&emsp;Huisnummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumber].valueString`  |
| 503 | &emsp;&emsp;Huisnummerletter | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 504 | &emsp;&emsp;Huisnummertoevoeging | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberLetter-houseNumberAddition].valueString`  |
| 505 | &emsp;&emsp;AanduidingBijNummer | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[houseNumberIndication].valueString`  |
| 506 | &emsp;&emsp;Postcode | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.postalCode`  |
| 507 | &emsp;&emsp;Woonplaats | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.city`  |
| 508 | &emsp;&emsp;Gemeente | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.district`  |
| 509 | &emsp;&emsp;Land | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.country.extension[countryCode].valueCodeableConcept`  |
| 510 | &emsp;&emsp;AdditioneleInformatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.line.extension[additionalInformation].valueString`  |
| 511 | &emsp;&emsp;AdresSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.use`  |
| 511 | &emsp;&emsp;AdresSoort | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address.type`  |
| 512 | &emsp;Rol | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[role]`  |
| 513 | &emsp;Relatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[relationship]`  |
| 514 | Gesprek gevoerd in bijzijn van (Patient) | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `subject`  |
| 515 | &emsp;Naamgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name`  |
| 516 | &emsp;&emsp;Voornamen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].given`  |
| 517 | &emsp;&emsp;Initialen | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].given`  |
| 518 | &emsp;&emsp;Roepnaam | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation-GivenName].given`  |
| 519 | &emsp;&emsp;Naamgebruik | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].use`  |
| 521 | &emsp;&emsp;&emsp;Voorvoegsels | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[prefix].valueString`  |
| 522 | &emsp;&emsp;&emsp;Achternaam | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[lastName].valueString`  |
| 524 | &emsp;&emsp;&emsp;VoorvoegselsPartner | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[partnerPrefix].valueString`  |
| 525 | &emsp;&emsp;&emsp;AchternaamPartner | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].family.extension[partnerLastName].valueString`  |
| 526 | &emsp;&emsp;Titels | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name[nameInformation].suffix`  |
| 554 | Gesprek gevoerd in bijzijn van (Contactpersoon) | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `participant[contactPerson].individual`  |
| 554 | Gesprek gevoerd in bijzijn van (Contactpersoon) | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 555 | &emsp;Naamgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name`  |
| 556 | &emsp;&emsp;Voornamen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 557 | &emsp;&emsp;Initialen | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].given`  |
| 558 | &emsp;&emsp;Roepnaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation-GivenName].given`  |
| 559 | &emsp;&emsp;Naamgebruik | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].use`  |
| 561 | &emsp;&emsp;&emsp;Voorvoegsels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[prefix].valueString`  |
| 562 | &emsp;&emsp;&emsp;Achternaam | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[lastName].valueString`  |
| 564 | &emsp;&emsp;&emsp;VoorvoegselsPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerPrefix].valueString`  |
| 565 | &emsp;&emsp;&emsp;AchternaamPartner | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].family.extension[partnerLastName].valueString`  |
| 566 | &emsp;&emsp;Titels | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name[nameInformation].suffix`  |
| 588 | &emsp;Rol | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[role]`  |
| 589 | &emsp;Relatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[relationship]`  |
| 590 | Belangrijkste doel van behandeling ([Meting]) | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | ``  |
| 591 | &emsp;Belangrijkste doel van behandeling ([MetingNaam]) | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | ``  |
| 592 | &emsp;Doel ([MetingWaarde]) | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `description`  |
| 596 | &emsp;[MeetDatumBeginTijd] | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `statusDate`  |
| 598 | &emsp;[Toelichting] | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `note.text`  |
| 602 | Behandelgrens (BehandelAanwijzing2) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | ``  |
| 603 | &emsp;BehandelBesluit | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.type`  |
| 604 | &emsp;Behandeling | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.code`  |
| 605 | &emsp;SpecificatieAnders | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `modifierExtension[specificationOther].value[x]`  |
| 606 | &emsp;MeestRecenteBespreekdatum | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `dateTime`  |
| 607 | &emsp;DatumBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.period.end`  |
| 608 | &emsp;RedenBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.extension[reasonForEnding].value[x]`  |
| 609 | &emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `sourceReference`  |
| 610 | &emsp;&emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 611 | &emsp;AfspraakPartij | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty]`  |
| 612 | &emsp;&emsp;Patient | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 613 | &emsp;&emsp;&emsp;Patient | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | ``  |
| 614 | &emsp;&emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 615 | &emsp;&emsp;&emsp;Contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 616 | &emsp;&emsp;Zorgverlener | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 617 | &emsp;&emsp;&emsp;Zorgverlener | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | ``  |
| 618 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `extension[comment].value[x]`  |
| 619 | Heeft de patient een ICD? | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `type`  |
| 619 | Heeft de patient een ICD? | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | ``  |
| 620 | ICD (MedischHulpmiddel) | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | ``  |
| 621 | &emsp;Product | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | ``  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `identifier[gs1ProductID]`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `identifier[hibcProductID]`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `udiCarrier[gs1UdiCarrier].carrierHRF`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `udiCarrier[hibcUdiCarrier].carrierHRF`  |
| 623 | &emsp;&emsp;ProductType van ICD | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `type`  |
| 624 | &emsp;ProductOmschrijving | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `note.text`  |
| 625 | &emsp;AnatomischeLocatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `bodySite`  |
| 626 | &emsp;&emsp;Locatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `bodySite`  |
| 627 | &emsp;&emsp;Lateraliteit | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `bodySite.extension[laterality].valueCodeableConcept`  |
| 628 | &emsp;Indicatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `reasonReference[indication]`  |
| 630 | &emsp;BeginDatum | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `timingPeriod.start`  |
| 631 | &emsp;EindDatum | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `timingPeriod.end`  |
| 632 | &emsp;Toelichting | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `note.text`  |
| 633 | &emsp;Locatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `extension[location].value[x]`  |
| 635 | &emsp;Zorgverlener | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `extension[healthProfessional].value[x]`  |
| 636 | &emsp;&emsp;Zorgverlener | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | ``  |
| 637 | Afspraak uitzetten ICD (BehandelAanwijzing2) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | ``  |
| 638 | &emsp;Afspraak uitzetten ICD (BehandelBesluit) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.type`  |
| 639 | &emsp;Behandeling van ICD (Behandeling) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.code.text`  |
| 641 | &emsp;MeestRecenteBespreekdatum | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `dateTime`  |
| 642 | &emsp;DatumBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.period.end`  |
| 643 | &emsp;RedenBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.extension[reasonForEnding]`  |
| 644 | &emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `extension[additionalAdvanceDirective].valueReference`  |
| 644 | &emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `sourceReference`  |
| 645 | &emsp;&emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 646 | &emsp;AfspraakPartij | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty]`  |
| 647 | &emsp;&emsp;Patient | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 648 | &emsp;&emsp;&emsp;Patient | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | ``  |
| 649 | &emsp;&emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 650 | &emsp;&emsp;&emsp;Contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 651 | &emsp;&emsp;Zorgverlener | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 652 | &emsp;&emsp;&emsp;Zorgverlener | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | ``  |
| 653 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `extension[comment].value[x]`  |
| 654 | Specifieke wensen ([Meting]) | Observation (<a href="StructureDefinition-ACP-SpecificCareWishes.html">ACPSpecificCareWishes</a>) | ``  |
| 655 | &emsp;Wens en verwachting patient ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-SpecificCareWishes.html">ACPSpecificCareWishes</a>) | `code`  |
| 656 | &emsp;Wens en verwachting patient ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-SpecificCareWishes.html">ACPSpecificCareWishes</a>) | `valueString`  |
| 657 | &emsp;Vaststellen wens en verwachting patiënt ([MeetMethode]) | Observation (<a href="StructureDefinition-ACP-SpecificCareWishes.html">ACPSpecificCareWishes</a>) | `method`  |
| 660 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-SpecificCareWishes.html">ACPSpecificCareWishes</a>) | `effective[x]`  |
| 666 | Gewenste plek van overlijden ([Meting]) | Observation (<a href="StructureDefinition-ACP-PreferredPlaceOfDeath.html">ACPPreferredPlaceOfDeath</a>) | ``  |
| 667 | &emsp;Gewenste plek van overlijden ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-PreferredPlaceOfDeath.html">ACPPreferredPlaceOfDeath</a>) | `code`  |
| 668 | &emsp;Voorkeursplek ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-PreferredPlaceOfDeath.html">ACPPreferredPlaceOfDeath</a>) | `valueCodeableConcept`  |
| 672 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-PreferredPlaceOfDeath.html">ACPPreferredPlaceOfDeath</a>) | `effective[x]`  |
| 674 | &emsp;[Toelichting] | Observation (<a href="StructureDefinition-ACP-PreferredPlaceOfDeath.html">ACPPreferredPlaceOfDeath</a>) | `note.text`  |
| 678 | Euthanasie standpunt ([Meting]) | Observation (<a href="StructureDefinition-ACP-PositionRegardingEuthanasia.html">ACPPositionRegardingEuthanasia</a>) | ``  |
| 679 | &emsp;Euthanasie standpunt ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-PositionRegardingEuthanasia.html">ACPPositionRegardingEuthanasia</a>) | `code`  |
| 680 | &emsp;Euthanasie standpunt ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-PositionRegardingEuthanasia.html">ACPPositionRegardingEuthanasia</a>) | `valueCodeableConcept`  |
| 684 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-PositionRegardingEuthanasia.html">ACPPositionRegardingEuthanasia</a>) | `effective[x]`  |
| 686 | &emsp;[Toelichting] | Observation (<a href="StructureDefinition-ACP-PositionRegardingEuthanasia.html">ACPPositionRegardingEuthanasia</a>) | `note.text`  |
| 690 | Euthanasieverklaring (Wilsverklaring) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 691 | &emsp;Euthanasieverklaring (WilsverklaringType) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.code`  |
| 692 | &emsp;WilsverklaringDatum | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `dateTime`  |
| 693 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder].value[x]`  |
| 695 | &emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 696 | &emsp;&emsp;Contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 697 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 698 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |
| 746 | Keuze orgaandonatie vastgelegd in donorregister? ([Meting]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | ``  |
| 747 | &emsp;Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `code`  |
| 748 | &emsp;Keuze orgaandonatie in donorregister ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `valueCodeableConcept`  |
| 752 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `effective[x]`  |
| 700 | Keuze orgaandonatie vastgelegd (Wilsverklaring) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 701 | &emsp;Orgaandonatie (WilsverklaringType) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.code`  |
| 702 | &emsp;WilsverklaringDatum | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `dateTime`  |
| 703 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder].value[x]`  |
| 705 | &emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 706 | &emsp;&emsp;Contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 707 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 708 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |
| 709 | Wat verder nog belangrijk is ([Meting]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | ``  |
| 710 | &emsp;Wat verder nog belangrijk is ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `code`  |
| 711 | &emsp;Wat verder nog belangrijk is ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `valueString`  |
| 715 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `effective[x]`  |
| 721 | Eerder vastgelegde behandelafspraken (Wilsverklaring) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 722 | &emsp;WilsverklaringType | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.code`  |
| 723 | &emsp;WilsverklaringDatum | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `dateTime`  |
| 724 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder].value[x]`  |
| 726 | &emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 727 | &emsp;&emsp;Contactpersoon | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 728 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 729 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |


##### Overview of Unmapped Elements

| ID | Name |
|---|---|
| 629 | Probleem |
| 634 | Zorgaanbieder |
| 694 | Probleem |
| 704 | Probleem |
| 725 | Probleem |
| 730 | Heeft de patient eerder behandelafspraken vastgelegd? |
| 731 | Heeft de patient eerder behandelafspraken vastgelegd? |
| 732 | Toelichting |
| 733 | Staan in eerder vastgelegde behandelafspraken andere wensen dan nu in deze verklaring? |
| 734 | Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken? |
| 735 | Patient gaat akkoord met het delen van deze behandelafspraken met andere betrokken hulpverleners |


##### Overview of Orphan Mappings

| ID | Resource | FHIR element |
|---|---|---|
| 000 | Procedure (<a href="StructureDefinition-ACP-Procedure.html">ACPProcedure</a>) | `` |

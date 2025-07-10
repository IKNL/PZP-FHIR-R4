##### Mappings by dataset ID

| Dataset ID | Dataset name | Resource | FHIR element |
|---|---|---|---|
| 351 | Patient | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | ``  |
| 352 | &emsp;Naamgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `name`  |
| 364 | &emsp;Adresgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `address`  |
| 376 | &emsp;Contactgegevens | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `telecom`  |
| 385 | &emsp;Identificatienummer | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `identifier`  |
| 386 | &emsp;Geboortedatum | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `birthDate`  |
| 387 | &emsp;Geslacht | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `gender`  |
| 387 | &emsp;Geslacht | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `gender.extension[genderCodelist].value[x]`  |
| 391 | Gesprek gevoerd door (Zorgverlener) | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | ``  |
| 391 | Gesprek gevoerd door (Zorgverlener) | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | ``  |
| 392 | &emsp;ZorgverlenerIdentificatienummer | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `identifier`  |
| 394 | &emsp;&emsp;Voornamen | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation-GivenName].given`  |
| 398 | &emsp;&emsp;Geslachtsnaam | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family`  |
| 399 | &emsp;&emsp;&emsp;Voorvoegsels | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family.extension[prefix]`  |
| 400 | &emsp;&emsp;&emsp;Achternaam | Practitioner (<a href="StructureDefinition-ACP-HealthProfessional-Practitioner.html">ACPHealthProfessionalPractitioner</a>) | `name[nameInformation].family.extension[lastName]`  |
| 405 | &emsp;Specialisme | PractitionerRole (<a href="StructureDefinition-ACP-HealthProfessional-PractitionerRole.html">ACPHealthProfessionalPractitionerRole</a>) | `specialty[specialty]`  |
| 431 | Wilsbekwaamheid (VrijheidsbeperkendeInterventie) | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | ``  |
| 432 | &emsp;Wilsbekwaam | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `extension[legallyCapable]`  |
| 433 | &emsp;WilsbekwaamToelichting | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `extension[legallyCapable]`  |
| 435 | &emsp;&emsp;JuridischeSituatie | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `reasonReference[legalSituation-LegalStatus]`  |
| 435 | &emsp;&emsp;JuridischeSituatie | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `reasonReference[legalSituation-Representation]`  |
| 436 | &emsp;SoortInterventie | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `code`  |
| 437 | &emsp;RedenVanToepassen | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `reasonCode`  |
| 439 | &emsp;Begin | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `performedPeriod.start`  |
| 439 | &emsp;Begin | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `performedDateTime`  |
| 440 | &emsp;Einde | Procedure (<a href="StructureDefinition-ACP-FreedomRestrictingIntervention.html">ACPFreedomRestrictingIntervention</a>) | `performedPeriod.end`  |
| 441 | Wettelijk vertegenwoordiger (Contactpersoon) | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | ``  |
| 442 | &emsp;Naamgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `name`  |
| 454 | &emsp;Contactgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `telecom`  |
| 463 | &emsp;Adresgegevens | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `address`  |
| 475 | &emsp;Rol | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[role]`  |
| 476 | &emsp;Relatie | RelatedPerson (<a href="StructureDefinition-ACP-ContactPerson.html">ACPContactPerson</a>) | `relationship[relationship]`  |
| 477 | Vertegenwoordiger is contactpersoon | Patient (<a href="StructureDefinition-ACP-Patient.html">ACPPatient</a>) | `contact.extension[relatedPerson]`  |
| 514 | Gesprek gevoerd in bijzijn van (Patient) | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `subject`  |
| 554 | Gesprek gevoerd in bijzijn van (Contactpersoon) | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `participant[contactPerson].individual`  |
| 590 | Belangrijkste doel van behandeling ([Meting]) | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | ``  |
| 591 | &emsp;Belangrijkste doel van behandeling ([MetingNaam]) | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `description`  |
| 596 | &emsp;[MeetDatumBeginTijd] | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `statusDate`  |
| 598 | &emsp;[Toelichting] | Goal (<a href="StructureDefinition-ACP-Medical-Policy-Goal.html">ACPMedicalPolicyGoal</a>) | `note.text`  |
| 602 | Behandelgrens (BehandelAanwijzing) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | ``  |
| 603 | &emsp;BehandelBesluit | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.type`  |
| 604 | &emsp;Behandeling | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.code`  |
| 605 | &emsp;SpecificatieAnders | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `modifierExtension[specificationOther]`  |
| 606 | &emsp;MeestRecenteBespreekdatum | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `dateTime`  |
| 607 | &emsp;DatumBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.period.end`  |
| 608 | &emsp;RedenBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.extension[reasonForEnding]`  |
| 609 | &emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `sourceReference`  |
| 611 | &emsp;AfspraakPartij | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty]`  |
| 612 | &emsp;&emsp;Patient | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 614 | &emsp;&emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 616 | &emsp;&emsp;Zorgverlener | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 618 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `extension[comment].value[x]`  |
| 618 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `extension[comment].value[x]`  |
| 620 | ICD (MedischHulpmiddel) | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | ``  |
| 620 | ICD (MedischHulpmiddel) | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | ``  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `identifier[gs1ProductID]`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `identifier[hibcProductID]`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `udiCarrier[gs1UdiCarrier].carrierHRF`  |
| 622 | &emsp;&emsp;ProductID | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `udiCarrier[hibcUdiCarrier].carrierHRF`  |
| 623 | &emsp;&emsp;ProductType van ICD | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `type`  |
| 624 | &emsp;ProductOmschrijving | Device (<a href="StructureDefinition-ACP-MedicalDevice.Product-ICD.html">ACPMedicalDeviceProductICD</a>) | `note.text`  |
| 625 | &emsp;AnatomischeLocatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `bodySite`  |
| 628 | &emsp;Indicatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `reasonReference[indication]`  |
| 630 | &emsp;BeginDatum | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `timingPeriod.start`  |
| 631 | &emsp;EindDatum | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `timingPeriod.end`  |
| 632 | &emsp;Toelichting | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `note.text`  |
| 633 | &emsp;Locatie | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `extension[location]`  |
| 635 | &emsp;Zorgverlener | DeviceUseStatement (<a href="StructureDefinition-ACP-MedicalDevice.html">ACPMedicalDevice</a>) | `extension[healthProfessional]`  |
| 637 | Afspraak uitzetten ICD (BehandelAanwijzing) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | ``  |
| 638 | &emsp;Afspraak uitzetten ICD (BehandelBesluit) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.type`  |
| 639 | &emsp;Behandeling van ICD (Behandeling) | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.code.text`  |
| 641 | &emsp;MeestRecenteBespreekdatum | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `dateTime`  |
| 642 | &emsp;DatumBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.period.end`  |
| 643 | &emsp;RedenBeeindigd | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.extension[reasonForEnding]`  |
| 644 | &emsp;Wilsverklaring | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `sourceReference`  |
| 646 | &emsp;AfspraakPartij | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty]`  |
| 647 | &emsp;&emsp;Patient | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 649 | &emsp;&emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
| 651 | &emsp;&emsp;Zorgverlener | Consent (<a href="StructureDefinition-ACP-TreatmentDirective.html">ACPTreatmentDirective</a>) | `provision.actor[agreementParty].reference`  |
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
| 693 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder]`  |
| 693 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 697 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 698 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |
| 700 | Keuze orgaandonatie vastgelegd (Wilsverklaring) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 701 | &emsp;Orgaandonatie (WilsverklaringType) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.code`  |
| 702 | &emsp;WilsverklaringDatum | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `dateTime`  |
| 703 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder]`  |
| 705 | &emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 705 | &emsp;Vertegenwoordiger | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.actor[representative].reference`  |
| 707 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 708 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |
| 709 | Wat verder nog belangrijk is ([Meting]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | ``  |
| 710 | &emsp;Wat verder nog belangrijk is ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `code`  |
| 711 | &emsp;Wat verder nog belangrijk is ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `valueString`  |
| 715 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-OtherImportantInformation.html">ACPOtherImportantInformation</a>) | `effective[x]`  |
| 721 | Eerder vastgelegde behandelafspraken (Wilsverklaring) | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | ``  |
| 722 | &emsp;WilsverklaringType | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `provision.code`  |
| 723 | &emsp;WilsverklaringDatum | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `dateTime`  |
| 724 | &emsp;Aandoening | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[disorder]`  |
| 728 | &emsp;WilsverklaringDocument | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `sourceAttachment`  |
| 729 | &emsp;Toelichting | Consent (<a href="StructureDefinition-ACP-AdvanceDirective.html">ACPAdvanceDirective</a>) | `extension[comment].value[x]`  |
| 736 | Datum van invullen | Encounter (<a href="StructureDefinition-ACP-Encounter.html">ACPEncounter</a>) | `period.start`  |
| 746 | Keuze orgaandonatie vastgelegd in donorregister? ([Meting]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | ``  |
| 747 | &emsp;Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `code`  |
| 748 | &emsp;Keuze orgaandonatie in donorregister ([MetingWaarde]) | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `valueCodeableConcept`  |
| 752 | &emsp;[MeetDatumBeginTijd] | Observation (<a href="StructureDefinition-ACP-OrganDonationChoiceRegistration.html">ACPOrganDonationChoiceRegistration</a>) | `effective[x]`  |


##### Overview of Unmapped Elements

| ID | Name |
|---|---|
| 350 | Informatiestandaard o.b.v. zibs2020 |
| 353 | Voornamen |
| 354 | Initialen |
| 355 | Roepnaam |
| 356 | Naamgebruik |
| 357 | Geslachtsnaam |
| 358 | Voorvoegsels |
| 359 | Achternaam |
| 360 | GeslachtsnaamPartner |
| 361 | VoorvoegselsPartner |
| 362 | AchternaamPartner |
| 363 | Titels |
| 365 | Straat |
| 366 | Huisnummer |
| 367 | Huisnummerletter |
| 368 | Huisnummertoevoeging |
| 369 | AanduidingBijNummer |
| 370 | Postcode |
| 371 | Woonplaats |
| 372 | Gemeente |
| 373 | Land |
| 374 | AdditioneleInformatie |
| 375 | AdresSoort |
| 377 | Telefoonnummers |
| 378 | Telefoonnummer |
| 379 | TelecomType |
| 380 | NummerSoort |
| 381 | Toelichting |
| 382 | EmailAdressen |
| 383 | EmailAdres |
| 384 | EmailSoort |
| 393 | Naamgegevens |
| 430 | ZorgverlenerRol |
| 434 | JuridischeSituatie |
| 438 | Instemming |
| 443 | Voornamen |
| 444 | Initialen |
| 445 | Roepnaam |
| 446 | Naamgebruik |
| 447 | Geslachtsnaam |
| 448 | Voorvoegsels |
| 449 | Achternaam |
| 450 | GeslachtsnaamPartner |
| 451 | VoorvoegselsPartner |
| 452 | AchternaamPartner |
| 453 | Titels |
| 455 | Telefoonnummers |
| 456 | Telefoonnummer |
| 457 | TelecomType |
| 458 | NummerSoort |
| 459 | Toelichting |
| 460 | EmailAdressen |
| 461 | EmailAdres |
| 462 | EmailSoort |
| 464 | Straat |
| 465 | Huisnummer |
| 466 | Huisnummerletter |
| 467 | Huisnummertoevoeging |
| 468 | AanduidingBijNummer |
| 469 | Postcode |
| 470 | Woonplaats |
| 471 | Gemeente |
| 472 | Land |
| 473 | AdditioneleInformatie |
| 474 | AdresSoort |
| 478 | Eerste contactpersoon (Contactpersoon) |
| 479 | Naamgegevens |
| 480 | Voornamen |
| 481 | Initialen |
| 482 | Roepnaam |
| 483 | Naamgebruik |
| 484 | Geslachtsnaam |
| 485 | Voorvoegsels |
| 486 | Achternaam |
| 487 | GeslachtsnaamPartner |
| 488 | VoorvoegselsPartner |
| 489 | AchternaamPartner |
| 490 | Titels |
| 491 | Contactgegevens |
| 492 | Telefoonnummers |
| 493 | Telefoonnummer |
| 494 | TelecomType |
| 495 | NummerSoort |
| 496 | Toelichting |
| 497 | EmailAdressen |
| 498 | EmailAdres |
| 499 | EmailSoort |
| 500 | Adresgegevens |
| 501 | Straat |
| 502 | Huisnummer |
| 503 | Huisnummerletter |
| 504 | Huisnummertoevoeging |
| 505 | AanduidingBijNummer |
| 506 | Postcode |
| 507 | Woonplaats |
| 508 | Gemeente |
| 509 | Land |
| 510 | AdditioneleInformatie |
| 511 | AdresSoort |
| 512 | Rol |
| 513 | Relatie |
| 515 | Naamgegevens |
| 516 | Voornamen |
| 517 | Initialen |
| 518 | Roepnaam |
| 519 | Naamgebruik |
| 520 | Geslachtsnaam |
| 521 | Voorvoegsels |
| 522 | Achternaam |
| 523 | GeslachtsnaamPartner |
| 524 | VoorvoegselsPartner |
| 525 | AchternaamPartner |
| 526 | Titels |
| 555 | Naamgegevens |
| 556 | Voornamen |
| 557 | Initialen |
| 558 | Roepnaam |
| 559 | Naamgebruik |
| 560 | Geslachtsnaam |
| 561 | Voorvoegsels |
| 562 | Achternaam |
| 563 | GeslachtsnaamPartner |
| 564 | VoorvoegselsPartner |
| 565 | AchternaamPartner |
| 566 | Titels |
| 588 | Rol |
| 589 | Relatie |
| 592 | Doel ([MetingWaarde]) |
| 610 | Wilsverklaring |
| 613 | Patient |
| 615 | Contactpersoon |
| 617 | Zorgverlener |
| 619 | Heeft de patiënt een ICD? |
| 621 | Product |
| 626 | Locatie |
| 627 | Lateraliteit |
| 629 | Probleem |
| 634 | Zorgaanbieder |
| 636 | Zorgverlener |
| 645 | Wilsverklaring |
| 648 | Patient |
| 650 | Contactpersoon |
| 652 | Zorgverlener |
| 653 | Toelichting |
| 694 | Probleem |
| 695 | Vertegenwoordiger |
| 696 | Contactpersoon |
| 704 | Probleem |
| 706 | Contactpersoon |
| 725 | Probleem |
| 726 | Vertegenwoordiger |
| 727 | Contactpersoon |
| 730 | Heeft de patiënt eerder behandelafspraken vastgelegd? |
| 731 | Heeft de patiënt eerder behandelafspraken vastgelegd? |
| 732 | Toelichting |
| 733 | Staan in eerder vastgelegde behandelafspraken andere wensen dan nu in deze verklaring? |
| 734 | Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken? |
| 735 | Patiënt gaat akkoord met het delen van deze behandelafspraken met andere betrokken hulpverleners |

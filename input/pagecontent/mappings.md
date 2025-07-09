### Mappings by Resource

| Resource (profile) | FHIR element | Functional ID | Functional name |
|---|---|---|---|
| Consent (ACPAdvanceDirective) | `` | 690 | Euthanasieverklaring (Wilsverklaring) |
| Consent (ACPAdvanceDirective) | `` | 700 | Keuze orgaandonatie vastgelegd (Wilsverklaring) |
| Consent (ACPAdvanceDirective) | `` | 721 | Eerder vastgelegde behandelafspraken (Wilsverklaring) |
| Consent (ACPAdvanceDirective) | `dateTime` | 692 | WilsverklaringDatum |
| Consent (ACPAdvanceDirective) | `dateTime` | 702 | WilsverklaringDatum |
| Consent (ACPAdvanceDirective) | `dateTime` | 723 | WilsverklaringDatum |
| Consent (ACPAdvanceDirective) | `extension[comment].value[x]` | 698 | Toelichting |
| Consent (ACPAdvanceDirective) | `extension[comment].value[x]` | 708 | Toelichting |
| Consent (ACPAdvanceDirective) | `extension[comment].value[x]` | 729 | Toelichting |
| Consent (ACPAdvanceDirective) | `extension[disorder]` | 693 | Aandoening |
| Consent (ACPAdvanceDirective) | `extension[disorder]` | 703 | Aandoening |
| Consent (ACPAdvanceDirective) | `extension[disorder]` | 724 | Aandoening |
| Consent (ACPAdvanceDirective) | `provision.actor[representative].reference` | 693 | Vertegenwoordiger |
| Consent (ACPAdvanceDirective) | `provision.actor[representative].reference` | 705 | Vertegenwoordiger |
| Consent (ACPAdvanceDirective) | `provision.actor[representative].reference` | 705 | Vertegenwoordiger |
| Consent (ACPAdvanceDirective) | `provision.code` | 691 | Euthanasieverklaring (WilsverklaringType) |
| Consent (ACPAdvanceDirective) | `provision.code` | 701 | Orgaandonatie (WilsverklaringType) |
| Consent (ACPAdvanceDirective) | `provision.code` | 722 | WilsverklaringType |
| Consent (ACPAdvanceDirective) | `sourceAttachment` | 697 | WilsverklaringDocument |
| Consent (ACPAdvanceDirective) | `sourceAttachment` | 707 | WilsverklaringDocument |
| Consent (ACPAdvanceDirective) | `sourceAttachment` | 728 | WilsverklaringDocument |
| RelatedPerson (ACPContactPerson) | `` | 441 | Wettelijk vertegenwoordiger (Contactpersoon) |
| RelatedPerson (ACPContactPerson) | `address` | 463 | Adresgegevens |
| RelatedPerson (ACPContactPerson) | `name` | 442 | Naamgegevens |
| RelatedPerson (ACPContactPerson) | `relationship[relationship]` | 476 | Relatie |
| RelatedPerson (ACPContactPerson) | `relationship[role]` | 475 | Rol |
| RelatedPerson (ACPContactPerson) | `telecom` | 454 | Contactgegevens |
| Observation (ACPDonorRegistration) | `` | 746 | Keuze orgaandonatie vastgelegd in donorregister? ([Meting]) |
| Observation (ACPDonorRegistration) | `code` | 747 | Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam]) |
| Observation (ACPDonorRegistration) | `effective[x]` | 752 | [MeetDatumBeginTijd] |
| Observation (ACPDonorRegistration) | `valueCodeableConcept` | 748 | Keuze orgaandonatie in donorregister ([MetingWaarde]) |
| Encounter (ACPEncounter) | `participant[contactPerson].individual` | 554 | Gesprek gevoerd in bijzijn van (Contactpersoon) |
| Encounter (ACPEncounter) | `period.start` | 736 | Datum van invullen |
| Encounter (ACPEncounter) | `subject` | 514 | Gesprek gevoerd in bijzijn van (Patient) |
| Procedure (ACPFreedomRestrictingIntervention) | `` | 431 | Wilsbekwaamheid (VrijheidsbeperkendeInterventie) |
| Procedure (ACPFreedomRestrictingIntervention) | `code` | 436 | SoortInterventie |
| Procedure (ACPFreedomRestrictingIntervention) | `extension[legallyCapable]` | 432 | Wilsbekwaam |
| Procedure (ACPFreedomRestrictingIntervention) | `extension[legallyCapable]` | 433 | WilsbekwaamToelichting |
| Procedure (ACPFreedomRestrictingIntervention) | `performedDateTime` | 439 | Begin |
| Procedure (ACPFreedomRestrictingIntervention) | `performedPeriod.end` | 440 | Einde |
| Procedure (ACPFreedomRestrictingIntervention) | `performedPeriod.start` | 439 | Begin |
| Procedure (ACPFreedomRestrictingIntervention) | `reasonCode` | 437 | RedenVanToepassen |
| Procedure (ACPFreedomRestrictingIntervention) | `reasonReference[legalSituation-LegalStatus]` | 435 | JuridischeSituatie |
| Procedure (ACPFreedomRestrictingIntervention) | `reasonReference[legalSituation-Representation]` | 435 | JuridischeSituatie |
| Practitioner (ACPHealthProfessionalPractitioner) | `` | 391 | Gesprek gevoerd door (Zorgverlener) |
| Practitioner (ACPHealthProfessionalPractitioner) | `identifier` | 392 | ZorgverlenerIdentificatienummer |
| Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation-GivenName].given` | 394 | Voornamen |
| Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family` | 398 | Geslachtsnaam |
| Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family.extension[lastName]` | 400 | Achternaam |
| Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family.extension[prefix]` | 399 | Voorvoegsels |
| PractitionerRole (ACPHealthProfessionalPractitionerRole) | `` | 391 | Gesprek gevoerd door (Zorgverlener) |
| PractitionerRole (ACPHealthProfessionalPractitionerRole) | `specialty[specialty]` | 405 | Specialisme |
| DeviceUseStatement (ACPMedicalDevice) | `` | 620 | ICD (MedischHulpmiddel) |
| DeviceUseStatement (ACPMedicalDevice) | `bodySite` | 625 | AnatomischeLocatie |
| DeviceUseStatement (ACPMedicalDevice) | `extension[healthProfessional]` | 635 | Zorgverlener |
| DeviceUseStatement (ACPMedicalDevice) | `extension[location]` | 633 | Locatie |
| DeviceUseStatement (ACPMedicalDevice) | `note.text` | 632 | Toelichting |
| DeviceUseStatement (ACPMedicalDevice) | `reasonReference[indication]` | 628 | Indicatie |
| DeviceUseStatement (ACPMedicalDevice) | `timingPeriod.end` | 631 | EndDate |
| DeviceUseStatement (ACPMedicalDevice) | `timingPeriod.start` | 630 | BeginDatum |
| Device (ACPMedicalDeviceProductICD) | `` | 620 | ICD (MedischHulpmiddel) |
| Device (ACPMedicalDeviceProductICD) | `identifier[gs1ProductID]` | 622 | ProductID |
| Device (ACPMedicalDeviceProductICD) | `identifier[hibcProductID]` | 622 | ProductID |
| Device (ACPMedicalDeviceProductICD) | `note.text` | 624 | ProductOmschrijving |
| Device (ACPMedicalDeviceProductICD) | `type` | 623 | ProductType van ICD |
| Device (ACPMedicalDeviceProductICD) | `udiCarrier[gs1UdiCarrier].carrierHRF` | 622 | ProductID |
| Device (ACPMedicalDeviceProductICD) | `udiCarrier[hibcUdiCarrier].carrierHRF` | 622 | ProductID |
| Goal (ACPMedicalPolicyGoal) | `` | 590 | Belangrijkste doel van behandeling ([Meting]) |
| Goal (ACPMedicalPolicyGoal) | `description` | 591 | Belangrijkste doel van behandeling ([MetingNaam]) |
| Goal (ACPMedicalPolicyGoal) | `statusDate` | 736 | Datum van invullen |
| Observation (ACPOtherImportantInformation) | `` | 709 | Wat verder nog belangrijk is ([Meting]) |
| Observation (ACPOtherImportantInformation) | `code` | 710 | Wat verder nog belangrijk is ([MetingNaam]) |
| Observation (ACPOtherImportantInformation) | `effective[x]` | 715 | [MeetDatumBeginTijd] |
| Observation (ACPOtherImportantInformation) | `valueString` | 711 | Wat verder nog belangrijk is ([MetingWaarde]) |
| Patient (ACPPatient) | `` | 351 | Patient |
| Patient (ACPPatient) | `address` | 364 | Adresgegevens |
| Patient (ACPPatient) | `birthDate` | 386 | Geboortedatum |
| Patient (ACPPatient) | `contact.extension[relatedPerson]` | 477 | Vertegenwoordiger is contactpersoon |
| Patient (ACPPatient) | `gender` | 387 | Geslacht |
| Patient (ACPPatient) | `gender.extension[genderCodelist].value[x]` | 387 | Geslacht |
| Patient (ACPPatient) | `identifier` | 385 | Identificatienummer |
| Patient (ACPPatient) | `name` | 352 | Naamgegevens |
| Patient (ACPPatient) | `telecom` | 376 | Contactgegevens |
| Observation (ACPPositionRegardingEuthanasia) | `` | 678 | Euthanasie standpunt ([Meting]) |
| Observation (ACPPositionRegardingEuthanasia) | `code` | 679 | Euthanasie standpunt ([MetingNaam]) |
| Observation (ACPPositionRegardingEuthanasia) | `effective[x]` | 684 | [MeetDatumBeginTijd] |
| Observation (ACPPositionRegardingEuthanasia) | `note.text` | 686 | [Toelichting] |
| Observation (ACPPositionRegardingEuthanasia) | `valueCodeableConcept` | 680 | Euthanasie standpunt ([MetingWaarde]) |
| Observation (ACPPreferredPlaceOfDeath) | `` | 666 | Gewenste plek van overlijden ([Meting])) |
| Observation (ACPPreferredPlaceOfDeath) | `code` | 667 | Gewenste plek van overlijden ([Meting]) |
| Observation (ACPPreferredPlaceOfDeath) | `effective[x]` | 672 | [MeetDatumBeginTijd] |
| Observation (ACPPreferredPlaceOfDeath) | `note.text` | 674 | [Toelichting] |
| Observation (ACPPreferredPlaceOfDeath) | `valueCodeableConcept` | 668 | Voorkeursplek ([MetingWaarde]) |
| Observation (ACPSpecificCareWishes) | `` | 654 | Specifieke wensen ([Meting]) |
| Observation (ACPSpecificCareWishes) | `code` | 655 | Wens en verwachting patient ([MetingNaam]) |
| Observation (ACPSpecificCareWishes) | `effective[x]` | 660 | [MeetDatumBeginTijd] |
| Observation (ACPSpecificCareWishes) | `method` | 657 | Vaststellen wens en verwachting patiënt ([MeetMethode]) |
| Observation (ACPSpecificCareWishes) | `valueString` | 656 | Wens en verwachting patient ([MetingWaarde]) |
| Consent (ACPTreatmentDirective) | `` | 602 | Behandelgrens (BehandelAanwijzing) |
| Consent (ACPTreatmentDirective) | `dateTime` | 606 | MeestRecenteBespreekdatum |
| Consent (ACPTreatmentDirective) | `extension[comment].value[x]` | 618 | Toelichting |
| Consent (ACPTreatmentDirective) | `modifierExtension[specificationOther]` | 605 | SpecificatieAnders |
| Consent (ACPTreatmentDirective) | `provision.actor[agreementParty]` | 611 | AfspraakPartij |
| Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference` | 612 | Patient |
| Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference` | 614 | Vertegenwoordiger |
| Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference` | 616 | Zorgverlener |
| Consent (ACPTreatmentDirective) | `provision.code` | 604 | Behandeling |
| Consent (ACPTreatmentDirective) | `provision.extension[reasonForEnding]` | 608 | RedenBeeindigd |
| Consent (ACPTreatmentDirective) | `provision.period.end` | 607 | DatumBeeindigd |
| Consent (ACPTreatmentDirective) | `provision.type` | 603 | BehandelBesluit |
| Consent (ACPTreatmentDirective) | `sourceReference` | 609 | Wilsverklaring |
| Consent (ACPTreatmentDirectiveICD) | `` | 637 | Afspraak uitzetten ICD (BehandelAanwijzing) |
| Consent (ACPTreatmentDirectiveICD) | `dateTime` | 641 | MeestRecenteBespreekdatum |
| Consent (ACPTreatmentDirectiveICD) | `extension[comment].value[x]` | 618 | Toelichting |
| Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty]` | 646 | AfspraakPartij |
| Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference` | 647 | Patient |
| Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference` | 649 | Vertegenwoordiger |
| Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference` | 651 | Zorgverlener |
| Consent (ACPTreatmentDirectiveICD) | `provision.code` | 639 | Behandeling van ICD (Behandeling) |
| Consent (ACPTreatmentDirectiveICD) | `provision.extension[reasonForEnding]` | 643 | RedenBeeindigd |
| Consent (ACPTreatmentDirectiveICD) | `provision.period.end` | 642 | DatumBeeindigd |
| Consent (ACPTreatmentDirectiveICD) | `provision.type` | 638 | Afspraak uitzetten ICD (BehandelBesluit) |
| Consent (ACPTreatmentDirectiveICD) | `sourceReference` | 644 | Wilsverklaring |


### Mappings by Functional ID

| Functional ID | Functional name | Resource (profile) | FHIR element  |
|---|---|---|---|
| 351 | Patient | Patient (ACPPatient) | ``   |
| 352 | Naamgegevens | Patient (ACPPatient) | `name`   |
| 364 | Adresgegevens | Patient (ACPPatient) | `address`   |
| 376 | Contactgegevens | Patient (ACPPatient) | `telecom`   |
| 385 | Identificatienummer | Patient (ACPPatient) | `identifier`   |
| 386 | Geboortedatum | Patient (ACPPatient) | `birthDate`   |
| 387 | Geslacht | Patient (ACPPatient) | `gender`   |
| 387 | Geslacht | Patient (ACPPatient) | `gender.extension[genderCodelist].value[x]`   |
| 391 | Gesprek gevoerd door (Zorgverlener) | Practitioner (ACPHealthProfessionalPractitioner) | ``   |
| 391 | Gesprek gevoerd door (Zorgverlener) | PractitionerRole (ACPHealthProfessionalPractitionerRole) | ``   |
| 392 | ZorgverlenerIdentificatienummer | Practitioner (ACPHealthProfessionalPractitioner) | `identifier`   |
| 394 | Voornamen | Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation-GivenName].given`   |
| 398 | Geslachtsnaam | Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family`   |
| 399 | Voorvoegsels | Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family.extension[prefix]`   |
| 400 | Achternaam | Practitioner (ACPHealthProfessionalPractitioner) | `name[nameInformation].family.extension[lastName]`   |
| 405 | Specialisme | PractitionerRole (ACPHealthProfessionalPractitionerRole) | `specialty[specialty]`   |
| 431 | Wilsbekwaamheid (VrijheidsbeperkendeInterventie) | Procedure (ACPFreedomRestrictingIntervention) | ``   |
| 432 | Wilsbekwaam | Procedure (ACPFreedomRestrictingIntervention) | `extension[legallyCapable]`   |
| 433 | WilsbekwaamToelichting | Procedure (ACPFreedomRestrictingIntervention) | `extension[legallyCapable]`   |
| 435 | JuridischeSituatie | Procedure (ACPFreedomRestrictingIntervention) | `reasonReference[legalSituation-LegalStatus]`   |
| 435 | JuridischeSituatie | Procedure (ACPFreedomRestrictingIntervention) | `reasonReference[legalSituation-Representation]`   |
| 436 | SoortInterventie | Procedure (ACPFreedomRestrictingIntervention) | `code`   |
| 437 | RedenVanToepassen | Procedure (ACPFreedomRestrictingIntervention) | `reasonCode`   |
| 439 | Begin | Procedure (ACPFreedomRestrictingIntervention) | `performedPeriod.start`   |
| 439 | Begin | Procedure (ACPFreedomRestrictingIntervention) | `performedDateTime`   |
| 440 | Einde | Procedure (ACPFreedomRestrictingIntervention) | `performedPeriod.end`   |
| 441 | Wettelijk vertegenwoordiger (Contactpersoon) | RelatedPerson (ACPContactPerson) | ``   |
| 442 | Naamgegevens | RelatedPerson (ACPContactPerson) | `name`   |
| 454 | Contactgegevens | RelatedPerson (ACPContactPerson) | `telecom`   |
| 463 | Adresgegevens | RelatedPerson (ACPContactPerson) | `address`   |
| 475 | Rol | RelatedPerson (ACPContactPerson) | `relationship[role]`   |
| 476 | Relatie | RelatedPerson (ACPContactPerson) | `relationship[relationship]`   |
| 477 | Vertegenwoordiger is contactpersoon | Patient (ACPPatient) | `contact.extension[relatedPerson]`   |
| 514 | Gesprek gevoerd in bijzijn van (Patient) | Encounter (ACPEncounter) | `subject`   |
| 554 | Gesprek gevoerd in bijzijn van (Contactpersoon) | Encounter (ACPEncounter) | `participant[contactPerson].individual`   |
| 590 | Belangrijkste doel van behandeling ([Meting]) | Goal (ACPMedicalPolicyGoal) | ``   |
| 591 | Belangrijkste doel van behandeling ([MetingNaam]) | Goal (ACPMedicalPolicyGoal) | `description`   |
| 602 | Behandelgrens (BehandelAanwijzing) | Consent (ACPTreatmentDirective) | ``   |
| 603 | BehandelBesluit | Consent (ACPTreatmentDirective) | `provision.type`   |
| 604 | Behandeling | Consent (ACPTreatmentDirective) | `provision.code`   |
| 605 | SpecificatieAnders | Consent (ACPTreatmentDirective) | `modifierExtension[specificationOther]`   |
| 606 | MeestRecenteBespreekdatum | Consent (ACPTreatmentDirective) | `dateTime`   |
| 607 | DatumBeeindigd | Consent (ACPTreatmentDirective) | `provision.period.end`   |
| 608 | RedenBeeindigd | Consent (ACPTreatmentDirective) | `provision.extension[reasonForEnding]`   |
| 609 | Wilsverklaring | Consent (ACPTreatmentDirective) | `sourceReference`   |
| 611 | AfspraakPartij | Consent (ACPTreatmentDirective) | `provision.actor[agreementParty]`   |
| 612 | Patient | Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference`   |
| 614 | Vertegenwoordiger | Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference`   |
| 616 | Zorgverlener | Consent (ACPTreatmentDirective) | `provision.actor[agreementParty].reference`   |
| 618 | Toelichting | Consent (ACPTreatmentDirective) | `extension[comment].value[x]`   |
| 618 | Toelichting | Consent (ACPTreatmentDirectiveICD) | `extension[comment].value[x]`   |
| 620 | ICD (MedischHulpmiddel) | Device (ACPMedicalDeviceProductICD) | ``   |
| 620 | ICD (MedischHulpmiddel) | DeviceUseStatement (ACPMedicalDevice) | ``   |
| 622 | ProductID | Device (ACPMedicalDeviceProductICD) | `identifier[gs1ProductID]`   |
| 622 | ProductID | Device (ACPMedicalDeviceProductICD) | `identifier[hibcProductID]`   |
| 622 | ProductID | Device (ACPMedicalDeviceProductICD) | `udiCarrier[gs1UdiCarrier].carrierHRF`   |
| 622 | ProductID | Device (ACPMedicalDeviceProductICD) | `udiCarrier[hibcUdiCarrier].carrierHRF`   |
| 623 | ProductType van ICD | Device (ACPMedicalDeviceProductICD) | `type`   |
| 624 | ProductOmschrijving | Device (ACPMedicalDeviceProductICD) | `note.text`   |
| 625 | AnatomischeLocatie | DeviceUseStatement (ACPMedicalDevice) | `bodySite`   |
| 628 | Indicatie | DeviceUseStatement (ACPMedicalDevice) | `reasonReference[indication]`   |
| 630 | BeginDatum | DeviceUseStatement (ACPMedicalDevice) | `timingPeriod.start`   |
| 631 | EndDate | DeviceUseStatement (ACPMedicalDevice) | `timingPeriod.end`   |
| 632 | Toelichting | DeviceUseStatement (ACPMedicalDevice) | `note.text`   |
| 633 | Locatie | DeviceUseStatement (ACPMedicalDevice) | `extension[location]`   |
| 635 | Zorgverlener | DeviceUseStatement (ACPMedicalDevice) | `extension[healthProfessional]`   |
| 637 | Afspraak uitzetten ICD (BehandelAanwijzing) | Consent (ACPTreatmentDirectiveICD) | ``   |
| 638 | Afspraak uitzetten ICD (BehandelBesluit) | Consent (ACPTreatmentDirectiveICD) | `provision.type`   |
| 639 | Behandeling van ICD (Behandeling) | Consent (ACPTreatmentDirectiveICD) | `provision.code`   |
| 641 | MeestRecenteBespreekdatum | Consent (ACPTreatmentDirectiveICD) | `dateTime`   |
| 642 | DatumBeeindigd | Consent (ACPTreatmentDirectiveICD) | `provision.period.end`   |
| 643 | RedenBeeindigd | Consent (ACPTreatmentDirectiveICD) | `provision.extension[reasonForEnding]`   |
| 644 | Wilsverklaring | Consent (ACPTreatmentDirectiveICD) | `sourceReference`   |
| 646 | AfspraakPartij | Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty]`   |
| 647 | Patient | Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference`   |
| 649 | Vertegenwoordiger | Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference`   |
| 651 | Zorgverlener | Consent (ACPTreatmentDirectiveICD) | `provision.actor[agreementParty].reference`   |
| 654 | Specifieke wensen ([Meting]) | Observation (ACPSpecificCareWishes) | ``   |
| 655 | Wens en verwachting patient ([MetingNaam]) | Observation (ACPSpecificCareWishes) | `code`   |
| 656 | Wens en verwachting patient ([MetingWaarde]) | Observation (ACPSpecificCareWishes) | `valueString`   |
| 657 | Vaststellen wens en verwachting patiënt ([MeetMethode]) | Observation (ACPSpecificCareWishes) | `method`   |
| 660 | [MeetDatumBeginTijd] | Observation (ACPSpecificCareWishes) | `effective[x]`   |
| 666 | Gewenste plek van overlijden ([Meting])) | Observation (ACPPreferredPlaceOfDeath) | ``   |
| 667 | Gewenste plek van overlijden ([Meting]) | Observation (ACPPreferredPlaceOfDeath) | `code`   |
| 668 | Voorkeursplek ([MetingWaarde]) | Observation (ACPPreferredPlaceOfDeath) | `valueCodeableConcept`   |
| 672 | [MeetDatumBeginTijd] | Observation (ACPPreferredPlaceOfDeath) | `effective[x]`   |
| 674 | [Toelichting] | Observation (ACPPreferredPlaceOfDeath) | `note.text`   |
| 678 | Euthanasie standpunt ([Meting]) | Observation (ACPPositionRegardingEuthanasia) | ``   |
| 679 | Euthanasie standpunt ([MetingNaam]) | Observation (ACPPositionRegardingEuthanasia) | `code`   |
| 680 | Euthanasie standpunt ([MetingWaarde]) | Observation (ACPPositionRegardingEuthanasia) | `valueCodeableConcept`   |
| 684 | [MeetDatumBeginTijd] | Observation (ACPPositionRegardingEuthanasia) | `effective[x]`   |
| 686 | [Toelichting] | Observation (ACPPositionRegardingEuthanasia) | `note.text`   |
| 690 | Euthanasieverklaring (Wilsverklaring) | Consent (ACPAdvanceDirective) | ``   |
| 691 | Euthanasieverklaring (WilsverklaringType) | Consent (ACPAdvanceDirective) | `provision.code`   |
| 692 | WilsverklaringDatum | Consent (ACPAdvanceDirective) | `dateTime`   |
| 693 | Aandoening | Consent (ACPAdvanceDirective) | `extension[disorder]`   |
| 693 | Vertegenwoordiger | Consent (ACPAdvanceDirective) | `provision.actor[representative].reference`   |
| 697 | WilsverklaringDocument | Consent (ACPAdvanceDirective) | `sourceAttachment`   |
| 698 | Toelichting | Consent (ACPAdvanceDirective) | `extension[comment].value[x]`   |
| 700 | Keuze orgaandonatie vastgelegd (Wilsverklaring) | Consent (ACPAdvanceDirective) | ``   |
| 701 | Orgaandonatie (WilsverklaringType) | Consent (ACPAdvanceDirective) | `provision.code`   |
| 702 | WilsverklaringDatum | Consent (ACPAdvanceDirective) | `dateTime`   |
| 703 | Aandoening | Consent (ACPAdvanceDirective) | `extension[disorder]`   |
| 705 | Vertegenwoordiger | Consent (ACPAdvanceDirective) | `provision.actor[representative].reference`   |
| 705 | Vertegenwoordiger | Consent (ACPAdvanceDirective) | `provision.actor[representative].reference`   |
| 707 | WilsverklaringDocument | Consent (ACPAdvanceDirective) | `sourceAttachment`   |
| 708 | Toelichting | Consent (ACPAdvanceDirective) | `extension[comment].value[x]`   |
| 709 | Wat verder nog belangrijk is ([Meting]) | Observation (ACPOtherImportantInformation) | ``   |
| 710 | Wat verder nog belangrijk is ([MetingNaam]) | Observation (ACPOtherImportantInformation) | `code`   |
| 711 | Wat verder nog belangrijk is ([MetingWaarde]) | Observation (ACPOtherImportantInformation) | `valueString`   |
| 715 | [MeetDatumBeginTijd] | Observation (ACPOtherImportantInformation) | `effective[x]`   |
| 721 | Eerder vastgelegde behandelafspraken (Wilsverklaring) | Consent (ACPAdvanceDirective) | ``   |
| 722 | WilsverklaringType | Consent (ACPAdvanceDirective) | `provision.code`   |
| 723 | WilsverklaringDatum | Consent (ACPAdvanceDirective) | `dateTime`   |
| 724 | Aandoening | Consent (ACPAdvanceDirective) | `extension[disorder]`   |
| 728 | WilsverklaringDocument | Consent (ACPAdvanceDirective) | `sourceAttachment`   |
| 729 | Toelichting | Consent (ACPAdvanceDirective) | `extension[comment].value[x]`   |
| 736 | Datum van invullen | Encounter (ACPEncounter) | `period.start`   |
| 736 | Datum van invullen | Goal (ACPMedicalPolicyGoal) | `statusDate`   |
| 746 | Keuze orgaandonatie vastgelegd in donorregister? ([Meting]) | Observation (ACPDonorRegistration) | ``   |
| 747 | Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam]) | Observation (ACPDonorRegistration) | `code`   |
| 748 | Keuze orgaandonatie in donorregister ([MetingWaarde]) | Observation (ACPDonorRegistration) | `valueCodeableConcept`   |
| 752 | [MeetDatumBeginTijd] | Observation (ACPDonorRegistration) | `effective[x]`   |

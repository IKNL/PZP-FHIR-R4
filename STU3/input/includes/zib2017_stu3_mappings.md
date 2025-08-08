#### Mappings by dataset ID

This table lists all ZIB2017 dataset elements in original order, including unmapped ones, filtered to in-scope STU3 resources.

| ID | Dataset name | Resource | FHIR element |
|---|---|---|---|
| 764 | Contact | Encounter | `Encounter` |
| 765 | &emsp;ContactType | Encounter | `Encounter.class` |
| 766 | &emsp;ContactMet | Encounter | `Encounter.participant.individual` |
| 807 | &emsp;&emsp;Gesprek gevoerd door (Zorgverlener) | Patient | `Patient.generalPractitioner` |
| 807 | &emsp;&emsp;Gesprek gevoerd door (Zorgverlener) | Practitioner | `Practitioner` |
| 770 | &emsp;BeginDatumTijd | Encounter | `Encounter.period.start` |
| 772 | &emsp;RedenContact |  |  |
| 775 | &emsp;&emsp;Verrichting | Encounter | `Encounter.diagnosis.condition` |
| 776 | &emsp;&emsp;&emsp;Verrichting | Procedure | `Procedure` |
| 797 | &emsp;&emsp;&emsp;&emsp;PZP gesprek (VerrichtingType) | Procedure | `Procedure.code` |
| 283 | ZIBRoot |  |  |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | RelatedPerson | `RelatedPerson.period` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Consent | `Consent.dateTime` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Encounter | `Encounter.period` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Procedure | `Procedure.performed[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | DeviceUseStatement | `DeviceUseStatement.whenUsed` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Procedure | `Procedure.performed[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Procedure | `Procedure.performed[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effectiveDateTime` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Consent | `Consent.dateTime` |
| 11 | Patient | Patient | `Patient` |
| 12 | &emsp;Naamgegevens | Patient | `Patient.name` |
| 223 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 226 | &emsp;&emsp;&emsp;GeslachtsnaamPartner |  |  |
| 14 | &emsp;Adresgegevens | Patient | `Patient.address` |
| 15 | &emsp;&emsp;Adresgegevens |  |  |
| 16 | &emsp;Contactgegevens | Patient | `Patient.telecom` |
| 17 | &emsp;&emsp;Contactgegevens |  |  |
| 18 | &emsp;Identificatienummer | Patient | `Patient.identifier` |
| 19 | &emsp;Geboortedatum | Patient | `Patient.birthDate` |
| 20 | &emsp;Geslacht | Patient | `Patient.gender` |
| 24 | Gesprek gevoerd door (Zorgverlener) | Patient | `Patient.generalPractitioner` |
| 24 | Gesprek gevoerd door (Zorgverlener) | Practitioner | `Practitioner` |
| 25 | &emsp;ZorgverlenerIdentificatienummer | Practitioner | `Practitioner.identifier` |
| 26 | &emsp;Naamgegevens | Practitioner | `Practitioner.name` |
| 233 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 28 | &emsp;Functie (Specialisme) | PractitionerRole | `PractitionerRole.specialty` |
| 758 | Wilsbekwaamheid m.b.t. medische behandelbeslissingen |  |  |
| 759 | &emsp;Wilsbekwaamheid m.b.t. medische behandelbeslissingen |  |  |
| 760 | &emsp;Toelichting |  |  |
| 36 | Wettelijk vertegenwoordiger (Contactpersoon) | Patient | `Patient.contact` |
| 36 | Wettelijk vertegenwoordiger (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 37 | &emsp;Naam wettelijk vertegenwoordiger (Naamgegevens) | Patient | `Patient.contact.name` |
| 37 | &emsp;Naam wettelijk vertegenwoordiger (Naamgegevens) | RelatedPerson | `RelatedPerson.name` |
| 243 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 246 | &emsp;&emsp;&emsp;GeslachtsnaamPartner |  |  |
| 39 | &emsp;Contactgegevens wettelijk vertegenwoordiger (Contactgegevens) | Patient | `Patient.contact.telecom` |
| 39 | &emsp;Contactgegevens wettelijk vertegenwoordiger (Contactgegevens) | RelatedPerson | `RelatedPerson.telecom` |
| 41 | &emsp;Adresgegevens | Patient | `Patient.contact.address` |
| 41 | &emsp;Adresgegevens | RelatedPerson | `RelatedPerson.address` |
| 42 | &emsp;&emsp;Adresgegevens |  |  |
| 43 | &emsp;Rol | Patient | `Patient.contact.relationship` |
| 43 | &emsp;Rol | Extension | `Extension.valueCodeableConcept` |
| 43 | &emsp;Rol | RelatedPerson | `RelatedPerson.extension` |
| 44 | &emsp;Relatie tot patient (Relatie) | Patient | `Patient.contact.relationship` |
| 44 | &emsp;Relatie tot patient (Relatie) | RelatedPerson | `RelatedPerson.relationship` |
| 1 | Vertegenwoordiger is contactpersoon |  |  |
| 45 | Eerste contactpersoon (Contactpersoon) | Patient | `Patient.contact` |
| 45 | Eerste contactpersoon (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 67 | &emsp;Naamgegevens | Patient | `Patient.contact.name` |
| 67 | &emsp;Naamgegevens | RelatedPerson | `RelatedPerson.name` |
| 260 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 263 | &emsp;&emsp;&emsp;GeslachtsnaamPartner |  |  |
| 69 | &emsp;Contactgegevens | Patient | `Patient.contact.telecom` |
| 69 | &emsp;Contactgegevens | RelatedPerson | `RelatedPerson.telecom` |
| 71 | &emsp;Adresgegevens | Patient | `Patient.contact.address` |
| 71 | &emsp;Adresgegevens | RelatedPerson | `RelatedPerson.address` |
| 72 | &emsp;&emsp;Adresgegevens |  |  |
| 73 | &emsp;Rol | Patient | `Patient.contact.relationship` |
| 73 | &emsp;Rol | Extension | `Extension.valueCodeableConcept` |
| 73 | &emsp;Rol | RelatedPerson | `RelatedPerson.extension` |
| 74 | &emsp;Relatie tot patient (Relatie) | Patient | `Patient.contact.relationship` |
| 74 | &emsp;Relatie tot patient (Relatie) | RelatedPerson | `RelatedPerson.relationship` |
| 305 | Gesprek gevoerd in bijzijn van (Patient) |  |  |
| 328 | &emsp;Naamgegevens | Patient | `Patient.name` |
| 329 | &emsp;&emsp;Naamgegevens |  |  |
| 330 | &emsp;&emsp;&emsp;Voornamen |  |  |
| 331 | &emsp;&emsp;&emsp;Initialen |  |  |
| 332 | &emsp;&emsp;&emsp;Roepnaam |  |  |
| 333 | &emsp;&emsp;&emsp;Naamgebruik |  |  |
| 334 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 335 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels |  |  |
| 336 | &emsp;&emsp;&emsp;&emsp;Achternaam |  |  |
| 337 | &emsp;&emsp;&emsp;GeslachtsnaamPartner |  |  |
| 338 | &emsp;&emsp;&emsp;&emsp;VoorvoegselsPartner |  |  |
| 339 | &emsp;&emsp;&emsp;&emsp;AchternaamPartner |  |  |
| 148 | Gesprek gevoerd in bijzijn van (Contactpersoon) | Patient | `Patient.contact` |
| 148 | Gesprek gevoerd in bijzijn van (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 149 | &emsp;Naamgegevens | Patient | `Patient.contact.name` |
| 149 | &emsp;Naamgegevens | RelatedPerson | `RelatedPerson.name` |
| 277 | &emsp;&emsp;&emsp;Geslachtsnaam |  |  |
| 280 | &emsp;&emsp;&emsp;GeslachtsnaamPartner |  |  |
| 155 | &emsp;Rol | Patient | `Patient.contact.relationship` |
| 155 | &emsp;Rol | Extension | `Extension.valueCodeableConcept` |
| 155 | &emsp;Rol | RelatedPerson | `RelatedPerson.extension` |
| 156 | &emsp;Relatie tot patient (Relatie) | Patient | `Patient.contact.relationship` |
| 156 | &emsp;Relatie tot patient (Relatie) | RelatedPerson | `RelatedPerson.relationship` |
| 157 | Belangrijkste doel van behandeling (AlgemeneMeting) | Observation | `Observation` |
| 160 | &emsp;Toelichting | Observation | `Observation.comment` |
| 161 | &emsp;MeetUitslag | Observation | `Observation.related` |
| 162 | &emsp;&emsp;MetingNaam voor Belangrijkste doel van behandeling | Observation | `Observation.code` |
| 163 | &emsp;&emsp;Doel (UitslagWaarde) | Observation | `Observation.value[x]` |
| 165 | &emsp;&emsp;UitslagDatumTijd | Observation | `Observation.effective[x]` |
| 54 | Behandelgrens (BehandelAanwijzing) | Consent | `Consent` |
| 55 | &emsp;Verificatie | Consent | `Consent.extension` |
| 56 | &emsp;&emsp;Geverifieerd | Consent | `Consent.extension.extension` |
| 57 | &emsp;&emsp;GeverifieerdBij | Consent | `Consent.extension.extension` |
| 58 | &emsp;&emsp;VerificatieDatum | Consent | `Consent.extension.extension` |
| 59 | &emsp;Behandeling | Consent | `Consent.extension` |
| 60 | &emsp;BehandelingToegestaan | Consent | `Consent.modifierExtension` |
| 61 | &emsp;Beperkingen | Consent | `Consent.except.extension` |
| 62 | &emsp;BeginDatum | Consent | `Consent.period.start` |
| 63 | &emsp;EindDatum | Consent | `Consent.period.end` |
| 64 | &emsp;Toelichting | Consent | `Consent.extension` |
| 65 | &emsp;Wilsverklaring | Consent | `Consent.extension.value[x]` |
| 65 | &emsp;Wilsverklaring | Consent | `Consent.source[x]` |
| 66 | &emsp;&emsp;Wilsverklaring |  |  |
| 218 | Heeft de patient een ICD? |  |  |
| 75 | ICD (MedischHulpmiddel) | DeviceUseStatement | `DeviceUseStatement` |
| 76 | &emsp;Product | DeviceUseStatement | `DeviceUseStatement.device` |
| 76 | &emsp;Product | Device | `Device` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.identifier` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.identifier` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.udi.deviceIdentifier` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.udi.carrierHRF` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.lotNumber` |
| 77 | &emsp;&emsp;ProductID | Device | `Device.expirationDate` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | DeviceUseStatement | `DeviceUseStatement.device` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 78 | &emsp;&emsp;ProductType van ICD | DeviceUseStatement | `DeviceUseStatement.device` |
| 78 | &emsp;&emsp;ProductType van ICD | Device | `Device.type` |
| 79 | &emsp;ProductOmschrijving | Device | `Device.note.text` |
| 80 | &emsp;BeginDatum | DeviceUseStatement | `DeviceUseStatement.whenUsed.start` |
| 81 | &emsp;Indicatie | DeviceUseStatement | `DeviceUseStatement.indication.extension` |
| 82 | &emsp;&emsp;Probleem |  |  |
| 83 | &emsp;Toelichting | DeviceUseStatement | `DeviceUseStatement.note.text` |
| 84 | &emsp;AnatomischeLocatie | DeviceUseStatement | `DeviceUseStatement.bodySite` |
| 84 | &emsp;AnatomischeLocatie | DeviceUseStatement | `DeviceUseStatement.bodySite` |
| 85 | &emsp;Lateraliteit | DeviceUseStatement | `DeviceUseStatement.bodySite.extension.valueCodeableConcept` |
| 86 | &emsp;Locatie | DeviceUseStatement | `DeviceUseStatement.extension` |
| 87 | &emsp;&emsp;Zorgaanbieder |  |  |
| 88 | &emsp;Zorgverlener | DeviceUseStatement | `DeviceUseStatement.extension` |
| 89 | &emsp;&emsp;Zorgverlener |  |  |
| 90 | Afspraak uitzetten ICD (BehandelAanwijzing) | Consent | `Consent` |
| 91 | &emsp;Verificatie | Consent | `Consent.extension` |
| 92 | &emsp;&emsp;Geverifieerd | Consent | `Consent.extension.extension` |
| 93 | &emsp;&emsp;GeverifieerdBij | Consent | `Consent.extension.extension` |
| 94 | &emsp;&emsp;VerificatieDatum | Consent | `Consent.extension.extension` |
| 95 | &emsp;Behandeling van uitzetten ICD | Consent | `Consent.extension` |
| 96 | &emsp;Afspraak uitzetten ICD (BehandelingToegestaan) | Consent | `Consent.modifierExtension` |
| 98 | &emsp;BeginDatum | Consent | `Consent.period.start` |
| 99 | &emsp;EindDatum | Consent | `Consent.period.end` |
| 100 | &emsp;Toelichting | Consent | `Consent.extension` |
| 101 | &emsp;Wilsverklaring | Consent | `Consent.extension.value[x]` |
| 101 | &emsp;Wilsverklaring | Consent | `Consent.source[x]` |
| 102 | &emsp;&emsp;Wilsverklaring |  |  |
| 190 | Specifieke wensen (AlgemeneMeting) |  |  |
| 202 | &emsp;MeetUitslag |  |  |
| 203 | &emsp;&emsp;Wens en verwachting patient (MetingNaam) |  |  |
| 204 | &emsp;&emsp;Wens en verwachting patient (UitslagWaarde) | Observation | `Observation.value[x]` |
| 205 | &emsp;&emsp;Vaststellen wens en verwachting patiënt (Meetmethode) | Observation | `Observation.method` |
| 206 | &emsp;&emsp;UitslagDatumTijd |  |  |
| 105 | Gewenste plek van overlijden (AlgemeneMeting) | Observation | `Observation` |
| 108 | &emsp;Toelichting | Observation | `Observation.comment` |
| 109 | &emsp;Vastgelegde keuze (MeetUitslag) | Observation | `Observation.related` |
| 110 | &emsp;&emsp;MetingNaam voor Gewenste plek van overlijden | Observation | `Observation.code` |
| 111 | &emsp;&emsp;Voorkeursplek (UitslagWaarde) | Observation | `Observation.value[x]` |
| 113 | &emsp;&emsp;UitslagDatumTijd | Observation | `Observation.effective[x]` |
| 114 | Euthanasie standpunt (AlgemeneMeting) | Observation | `Observation` |
| 117 | &emsp;Toelichting | Observation | `Observation.comment` |
| 118 | &emsp;Vastgelegde keuze (MeetUitslag) | Observation | `Observation.related` |
| 119 | &emsp;&emsp;MetingNaam voor Euthanasie standpunt | Observation | `Observation.code` |
| 120 | &emsp;&emsp;Standpunt (UitslagWaarde) | Observation | `Observation.value[x]` |
| 122 | &emsp;&emsp;UitslagDatumTijd | Observation | `Observation.effective[x]` |
| 166 | Euthanasieverklaring (Wilsverklaring) | Consent | `Consent` |
| 175 | &emsp;Euthanasieverklaring (WilsverklaringType) | Consent | `Consent.category` |
| 176 | &emsp;WilsverklaringDatum | Consent | `Consent.dateTime` |
| 177 | &emsp;Aandoening | Consent | `Consent.extension` |
| 178 | &emsp;&emsp;Probleem |  |  |
| 179 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
| 180 | &emsp;&emsp;Contactpersoon |  |  |
| 181 | &emsp;WilsverklaringDocument | Consent | `Consent.source[x]` |
| 182 | &emsp;Toelichting | Consent | `Consent.extension` |
| 737 | Keuze orgaandonatie vastgelegd in donorregister? (AlgemeneMeting) | Observation | `Observation` |
| 741 | &emsp;MeetUitslag | Observation | `Observation.related` |
| 742 | &emsp;&emsp;MetingNaam voor Keuze orgaandonatie vastgelegd in donorregister? | Observation | `Observation.code` |
| 743 | &emsp;&emsp;Keuze orgaandonatie in donorregister (UitslagWaarde) | Observation | `Observation.value[x]` |
| 123 | Keuze orgaandonatie vastgelegd (Wilsverklaring) | Consent | `Consent` |
| 124 | &emsp;Orgaandonatie (WilsverklaringType) | Consent | `Consent.category` |
| 125 | &emsp;WilsverklaringDatum | Consent | `Consent.dateTime` |
| 126 | &emsp;Aandoening | Consent | `Consent.extension` |
| 127 | &emsp;&emsp;Probleem |  |  |
| 128 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
| 129 | &emsp;&emsp;Contactpersoon |  |  |
| 130 | &emsp;WilsverklaringDocument | Consent | `Consent.source[x]` |
| 131 | &emsp;Toelichting | Consent | `Consent.extension` |
| 132 | Wat verder nog belangrijk is (AlgemeneMeting) | Observation | `Observation` |
| 211 | &emsp;MeetUitslag | Observation | `Observation.related` |
| 212 | &emsp;&emsp;MetingNaam voor Wat verder nog belangrijk is | Observation | `Observation.code` |
| 213 | &emsp;&emsp;Wat verder nog belangrijk is (UitslagWaarde) | Observation | `Observation.value[x]` |
| 215 | &emsp;&emsp;UitslagDatumTijd | Observation | `Observation.effective[x]` |
| 139 | Eerder vastgelegde behandelafspraken (Wilsverklaring) | Consent | `Consent` |
| 140 | &emsp;WilsverklaringType | Consent | `Consent.category` |
| 141 | &emsp;WilsverklaringDatum | Consent | `Consent.dateTime` |
| 142 | &emsp;Aandoening | Consent | `Consent.extension` |
| 143 | &emsp;&emsp;Probleem |  |  |
| 144 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
| 145 | &emsp;&emsp;Contactpersoon |  |  |
| 146 | &emsp;WilsverklaringDocument | Consent | `Consent.source[x]` |
| 147 | &emsp;Toelichting | Consent | `Consent.extension` |
| 183 | Heeft de patient eerder behandelafspraken vastgelegd? |  |  |
| 207 | &emsp;Heeft de patient eerder behandelafspraken vastgelegd? |  |  |
| 184 | &emsp;Toelichting |  |  |
| 189 | Staan in eerder vastgelegde behandelafspraken andere wensen dan nu in deze verklaring? |  |  |
| 187 | Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken? |  |  |
| 188 | Patient gaat akkoord met het delen van deze behandelafspraken met andere betrokken hulpverleners |  |  |

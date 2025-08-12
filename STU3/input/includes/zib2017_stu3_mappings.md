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
| 772 | &emsp;RedenContact | Encounter | `Encounter.diagnosis.condition` |
| 775 | &emsp;&emsp;Verrichting | Encounter | `Encounter.diagnosis.condition` |
| 776 | &emsp;&emsp;&emsp;Verrichting | Procedure | `Procedure` |
| 797 | &emsp;&emsp;&emsp;&emsp;PZP gesprek (VerrichtingType) | Procedure | `Procedure.code` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effective[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | RelatedPerson | `RelatedPerson.period` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Consent | `Consent.dateTime` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Encounter | `Encounter.period` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Procedure | `Procedure.performed[x]` |
| 304 | &emsp;Datum van invullen (DatumTijd) | DeviceUseStatement | `DeviceUseStatement.whenUsed` |
| 304 | &emsp;Datum van invullen (DatumTijd) | Observation | `Observation.effectiveDateTime` |
| 11 | Patient | Patient | `Patient` |
| 12 | &emsp;Naamgegevens | HumanName | `HumanName` |
| 12 | &emsp;Naamgegevens | Patient | `Patient.name` |
| 13 | &emsp;&emsp;Naamgegevens | HumanName | `HumanName` |
| 219 | &emsp;&emsp;&emsp;Voornamen | HumanName | `HumanName.given` |
| 220 | &emsp;&emsp;&emsp;Initialen | HumanName | `HumanName.given` |
| 221 | &emsp;&emsp;&emsp;Roepnaam | HumanName | `HumanName.given` |
| 222 | &emsp;&emsp;&emsp;Naamgebruik | HumanName | `HumanName.extension` |
| 224 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels | HumanName | `HumanName.family.extension` |
| 225 | &emsp;&emsp;&emsp;&emsp;Achternaam | HumanName | `HumanName.family.extension` |
| 227 | &emsp;&emsp;&emsp;&emsp;VoorvoegselsPartner | HumanName | `HumanName.family.extension` |
| 228 | &emsp;&emsp;&emsp;&emsp;AchternaamPartner | HumanName | `HumanName.family.extension` |
| 14 | &emsp;Adresgegevens | Address | `Address` |
| 14 | &emsp;Adresgegevens | Patient | `Patient.address` |
| 16 | &emsp;Contactgegevens | ContactPoint | `ContactPoint` |
| 16 | &emsp;Contactgegevens | Patient | `Patient.telecom` |
| 18 | &emsp;Identificatienummer | Patient | `Patient.identifier` |
| 19 | &emsp;Geboortedatum | Patient | `Patient.birthDate` |
| 20 | &emsp;Geslacht | Patient | `Patient.gender` |
| 24 | Gesprek gevoerd door (Zorgverlener) | Patient | `Patient.generalPractitioner` |
| 24 | Gesprek gevoerd door (Zorgverlener) | Practitioner | `Practitioner` |
| 25 | &emsp;ZorgverlenerIdentificatienummer | Practitioner | `Practitioner.identifier` |
| 26 | &emsp;Naamgegevens | Practitioner | `Practitioner.name` |
| 27 | &emsp;&emsp;Naamgegevens | HumanName | `HumanName` |
| 229 | &emsp;&emsp;&emsp;Voornamen | HumanName | `HumanName.given` |
| 234 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels | HumanName | `HumanName.family.extension` |
| 235 | &emsp;&emsp;&emsp;&emsp;Achternaam | HumanName | `HumanName.family.extension` |
| 28 | &emsp;Functie (Specialisme) | PractitionerRole | `PractitionerRole.specialty` |
| 36 | Wettelijk vertegenwoordiger (Contactpersoon) | Patient | `Patient.contact` |
| 36 | Wettelijk vertegenwoordiger (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 37 | &emsp;Naam wettelijk vertegenwoordiger (Naamgegevens) | Patient | `Patient.contact.name` |
| 37 | &emsp;Naam wettelijk vertegenwoordiger (Naamgegevens) | RelatedPerson | `RelatedPerson.name` |
| 38 | &emsp;&emsp;Naamgegevens | HumanName | `HumanName` |
| 239 | &emsp;&emsp;&emsp;Voornamen | HumanName | `HumanName.given` |
| 240 | &emsp;&emsp;&emsp;Initialen | HumanName | `HumanName.given` |
| 241 | &emsp;&emsp;&emsp;Roepnaam | HumanName | `HumanName.given` |
| 242 | &emsp;&emsp;&emsp;Naamgebruik | HumanName | `HumanName.extension` |
| 244 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels | HumanName | `HumanName.family.extension` |
| 245 | &emsp;&emsp;&emsp;&emsp;Achternaam | HumanName | `HumanName.family.extension` |
| 247 | &emsp;&emsp;&emsp;&emsp;VoorvoegselsPartner | HumanName | `HumanName.family.extension` |
| 248 | &emsp;&emsp;&emsp;&emsp;AchternaamPartner | HumanName | `HumanName.family.extension` |
| 39 | &emsp;Contactgegevens wettelijk vertegenwoordiger (Contactgegevens) | Patient | `Patient.contact.telecom` |
| 39 | &emsp;Contactgegevens wettelijk vertegenwoordiger (Contactgegevens) | RelatedPerson | `RelatedPerson.telecom` |
| 40 | &emsp;&emsp;Contactgegevens | ContactPoint | `ContactPoint` |
| 250 | &emsp;&emsp;&emsp;&emsp;Telefoonnummer | ContactPoint | `ContactPoint.value` |
| 251 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.extension.valueCodeableConcept` |
| 251 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.system` |
| 251 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.use` |
| 252 | &emsp;&emsp;&emsp;&emsp;NummerSoort | ContactPoint | `ContactPoint.use` |
| 254 | &emsp;&emsp;&emsp;&emsp;EmailAdres | ContactPoint | `ContactPoint.value` |
| 255 | &emsp;&emsp;&emsp;&emsp;EmailSoort | ContactPoint | `ContactPoint.system` |
| 255 | &emsp;&emsp;&emsp;&emsp;EmailSoort | ContactPoint | `ContactPoint.use` |
| 41 | &emsp;Adresgegevens | Patient | `Patient.contact.address` |
| 41 | &emsp;Adresgegevens | RelatedPerson | `RelatedPerson.address` |
| 43 | &emsp;Rol | Patient | `Patient.contact.relationship` |
| 43 | &emsp;Rol | Extension | `Extension.valueCodeableConcept` |
| 43 | &emsp;Rol | RelatedPerson | `RelatedPerson.extension` |
| 44 | &emsp;Relatie tot patient (Relatie) | Patient | `Patient.contact.relationship` |
| 44 | &emsp;Relatie tot patient (Relatie) | RelatedPerson | `RelatedPerson.relationship` |
| 45 | Eerste contactpersoon (Contactpersoon) | Patient | `Patient.contact` |
| 45 | Eerste contactpersoon (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 67 | &emsp;Naamgegevens | Patient | `Patient.contact.name` |
| 67 | &emsp;Naamgegevens | RelatedPerson | `RelatedPerson.name` |
| 68 | &emsp;&emsp;Naamgegevens | HumanName | `HumanName` |
| 256 | &emsp;&emsp;&emsp;Voornamen | HumanName | `HumanName.given` |
| 257 | &emsp;&emsp;&emsp;Initialen | HumanName | `HumanName.given` |
| 258 | &emsp;&emsp;&emsp;Roepnaam | HumanName | `HumanName.given` |
| 259 | &emsp;&emsp;&emsp;Naamgebruik | HumanName | `HumanName.extension` |
| 261 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels | HumanName | `HumanName.family.extension` |
| 262 | &emsp;&emsp;&emsp;&emsp;Achternaam | HumanName | `HumanName.family.extension` |
| 264 | &emsp;&emsp;&emsp;&emsp;VoorvoegselsPartner | HumanName | `HumanName.family.extension` |
| 265 | &emsp;&emsp;&emsp;&emsp;AchternaamPartner | HumanName | `HumanName.family.extension` |
| 69 | &emsp;Contactgegevens | Patient | `Patient.contact.telecom` |
| 69 | &emsp;Contactgegevens | RelatedPerson | `RelatedPerson.telecom` |
| 70 | &emsp;&emsp;Contactgegevens | ContactPoint | `ContactPoint` |
| 267 | &emsp;&emsp;&emsp;&emsp;Telefoonnummer | ContactPoint | `ContactPoint.value` |
| 268 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.extension.valueCodeableConcept` |
| 268 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.system` |
| 268 | &emsp;&emsp;&emsp;&emsp;TelecomType | ContactPoint | `ContactPoint.use` |
| 269 | &emsp;&emsp;&emsp;&emsp;NummerSoort | ContactPoint | `ContactPoint.use` |
| 271 | &emsp;&emsp;&emsp;&emsp;EmailAdres | ContactPoint | `ContactPoint.value` |
| 272 | &emsp;&emsp;&emsp;&emsp;EmailSoort | ContactPoint | `ContactPoint.system` |
| 272 | &emsp;&emsp;&emsp;&emsp;EmailSoort | ContactPoint | `ContactPoint.use` |
| 71 | &emsp;Adresgegevens | Patient | `Patient.contact.address` |
| 71 | &emsp;Adresgegevens | RelatedPerson | `RelatedPerson.address` |
| 73 | &emsp;Rol | Patient | `Patient.contact.relationship` |
| 73 | &emsp;Rol | Extension | `Extension.valueCodeableConcept` |
| 73 | &emsp;Rol | RelatedPerson | `RelatedPerson.extension` |
| 74 | &emsp;Relatie tot patient (Relatie) | Patient | `Patient.contact.relationship` |
| 74 | &emsp;Relatie tot patient (Relatie) | RelatedPerson | `RelatedPerson.relationship` |
| 328 | &emsp;Naamgegevens | HumanName | `HumanName` |
| 328 | &emsp;Naamgegevens | Patient | `Patient.name` |
| 148 | Gesprek gevoerd in bijzijn van (Contactpersoon) | Patient | `Patient.contact` |
| 148 | Gesprek gevoerd in bijzijn van (Contactpersoon) | RelatedPerson | `RelatedPerson` |
| 149 | &emsp;Naamgegevens | Patient | `Patient.contact.name` |
| 149 | &emsp;Naamgegevens | RelatedPerson | `RelatedPerson.name` |
| 150 | &emsp;&emsp;Naamgegevens | HumanName | `HumanName` |
| 273 | &emsp;&emsp;&emsp;Voornamen | HumanName | `HumanName.given` |
| 274 | &emsp;&emsp;&emsp;Initialen | HumanName | `HumanName.given` |
| 275 | &emsp;&emsp;&emsp;Roepnaam | HumanName | `HumanName.given` |
| 276 | &emsp;&emsp;&emsp;Naamgebruik | HumanName | `HumanName.extension` |
| 278 | &emsp;&emsp;&emsp;&emsp;Voorvoegsels | HumanName | `HumanName.family.extension` |
| 279 | &emsp;&emsp;&emsp;&emsp;Achternaam | HumanName | `HumanName.family.extension` |
| 281 | &emsp;&emsp;&emsp;&emsp;VoorvoegselsPartner | HumanName | `HumanName.family.extension` |
| 282 | &emsp;&emsp;&emsp;&emsp;AchternaamPartner | HumanName | `HumanName.family.extension` |
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
| 78 | &emsp;&emsp;ProductType van ICD | DeviceUseStatement | `DeviceUseStatement.device` |
| 79 | &emsp;ProductOmschrijving | Device | `Device.note.text` |
| 80 | &emsp;BeginDatum | DeviceUseStatement | `DeviceUseStatement.whenUsed.start` |
| 81 | &emsp;Indicatie | DeviceUseStatement | `DeviceUseStatement.indication.extension` |
| 83 | &emsp;Toelichting | DeviceUseStatement | `DeviceUseStatement.note.text` |
| 84 | &emsp;AnatomischeLocatie | DeviceUseStatement | `DeviceUseStatement.bodySite` |
| 85 | &emsp;Lateraliteit | DeviceUseStatement | `DeviceUseStatement.bodySite.extension.valueCodeableConcept` |
| 86 | &emsp;Locatie | DeviceUseStatement | `DeviceUseStatement.extension` |
| 88 | &emsp;Zorgverlener | DeviceUseStatement | `DeviceUseStatement.extension` |
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
| 204 | &emsp;&emsp;Wens en verwachting patient (UitslagWaarde) | Observation | `Observation.value[x]` |
| 205 | &emsp;&emsp;Vaststellen wens en verwachting patiënt (Meetmethode) | Observation | `Observation.method` |
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
| 179 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
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
| 128 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
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
| 144 | &emsp;Vertegenwoordiger | Consent | `Consent.consentingParty` |
| 146 | &emsp;WilsverklaringDocument | Consent | `Consent.source[x]` |
| 147 | &emsp;Toelichting | Consent | `Consent.extension` |

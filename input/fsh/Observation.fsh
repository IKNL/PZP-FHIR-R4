Profile: ACPSpecificCareWishes
Parent: Observation
Id: ACP-SpecificCareWishes
Title: "Specific Care Wishes"
Description: "What, according to the patient, should healthcare providers know to provide good care? Does this patient have specific wishes regarding their care (including cultural, religious, social, and spiritual aspects)? The patient's wishes and expectations concerning their treatment."
* insert MetaRules
* encounter only Reference(Encounter)
* subject only Reference(Patient)
* code = $snomed#153851000146100 // TODO -- check if there is a international code for this?
* value[x] only string
* method = $snomed#370819000 // TODO -- check if we want this code to be present and if it actually maps to Observation.method Display: "Vaststellen van persoonlijke waarden en wensen met betrekking tot zorg" 

Mapping: MapACPSpecificCareWishes
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPSpecificCareWishes
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "654" "Specifieke wensen ([Meting])"
* code -> "655" "Wens en verwachting patient ([MetingNaam])"
* valueString -> "656" "Wens en verwachting patient ([MetingWaarde])"
* method -> "657" "Vaststellen wens en verwachting patiënt ([MeetMethode])"
* effective[x] -> "660" "[MeetDatumBeginTijd]"


Instance: F1-ACP-SpecificCareWishes
InstanceOf: ACPSpecificCareWishes
Title: "F1 ACP Specific Care Wishes"
Usage: #example
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#153851000146100
* valueString = "Hendrik wil er alles aan doen om zo lang mogelijk in goede gezondheid te kunnen leven. Hij probeert regelmatig te sporten en zou graag willen blijven hardlopen. Broer Michiel woont om de hoek en is erg betrokken bij het proces van Hendrik"
* effectiveDateTime = "2020-10-01"
* method = $snomed#370819000


Profile: ACPPreferredPlaceOfDeath
Parent: Observation
Id: ACP-PreferredPlaceOfDeath
Title: "Preferred Place Of Death"
Description: "The preferred place of death. This is the place where the patient prefers to die, if possible. The preferred place of death can be a home, a hospital, a nursing home, or another location."
* insert MetaRules
* encounter only Reference(Encounter)
* subject only Reference(Patient)
* code = $snomed#395091006 
* value[x] only CodeableConcept 
* value[x] from ACPPreferredPlaceOfDeathVS (extensible) // TODO - there is no binding strenght in dataset.

Mapping: MapACPSPreferredPlaceOfDeath
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPPreferredPlaceOfDeath
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "666" "Gewenste plek van overlijden ([Meting]))"
* code -> "667" "Gewenste plek van overlijden ([Meting])"
* valueCodeableConcept -> "668" "Voorkeursplek ([MetingWaarde])"
* effective[x] -> "672" "[MeetDatumBeginTijd]"
* note.text -> "674" "[Toelichting]"

Instance: F1-ACP-PreferredPlaceOfDeath-Unknown
InstanceOf: ACPPreferredPlaceOfDeath
Title: "F1 ACP Preferred Place Of Death Unknown"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "023ba125-94c3-492c-8379-958ac9fbb9d6"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#395091006
// * valueCodeableConcept = $v3-NullFlavor#UNK  -- Cannot have a value[x] if you have data absent reason
* dataAbsentReason = $DataAbsentReason#asked-unknown // TODO  This seems like a good fit for "Nog Onbekend". Add mapping to element? Could leave out valueCodeableConcept and use dataAbsentReason only.
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"

Profile: ACPPositionRegardingEuthanasia
Parent: Observation
Id: ACP-PositionRegardingEuthanasia
Title: "Position Regarding Euthanasia"
Description: "Position Regarding Euthanasia"
* insert MetaRules
* encounter only Reference(Encounter)
* subject only Reference(Patient)
* code = $snomed#340171000146104 // TODO -- check if there is a international code for this?
* value[x] only CodeableConcept
* value[x] ^definition = "Position regarding euthanesia."
* value[x] from ACPEuthanasiaStatementVS (extensible) // TODO - there is no binding strenght in dataset.
* note.text ^definition = "Comment accompanying position regarding euthanesia."

Mapping: MapACPPositionRegardingEuthanasia
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPPositionRegardingEuthanasia
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "678" "Euthanasie standpunt ([Meting])"
* code -> "679" "Euthanasie standpunt ([MetingNaam])"
* valueCodeableConcept -> "680" "Euthanasie standpunt ([MetingWaarde])"
* effective[x] -> "684" "[MeetDatumBeginTijd]"
* note.text -> "686" "[Toelichting]"

Instance: F1-ACP-PositionRegardingEuthanasia-Unknown
InstanceOf: ACPPositionRegardingEuthanasia
Title: "F1 ACP Position Regarding Euthanasia Unknown"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f2314b60-1b52-4f29-b231-8b74869fc34b"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#340171000146104
* valueCodeableConcept = $v3-NullFlavor#UNK
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"

Profile: ACPOrganDonationChoiceRegistration
Parent: Observation
Id: ACP-OrganDonationChoiceRegistration
Title: "Donor donation choice registration in donor register"
Description: "Donor donation choice registration in donor register."
* insert MetaRules
* encounter only Reference(Encounter)
* subject only Reference(Patient)
* code = $snomed#TODO // TODO -- no code in dataset?
* value[x] only CodeableConcept
* value[x] ^definition = "Organ donation choice recorded in donor register."
* value[x] from ACPYesNoUnknownVS (required) // TODO - there is no binding strenght in dataset.

Mapping: MapACPOrganDonationChoiceRegistration
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPOrganDonationChoiceRegistration
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "746" "Keuze orgaandonatie vastgelegd in donorregister? ([Meting])"
* code -> "747" "Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam])"
* valueCodeableConcept -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
* effective[x] -> "752" "[MeetDatumBeginTijd]"

Instance: F1-ACP-OrganDonationChoiceRegistration-Yes
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "F1 ACP Donor Registration Yes"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "31952dca-757c-4e4e-b7f6-fab66a79deba"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#TODO
* valueCodeableConcept = $snomed#373066001
* effectiveDateTime = "2020-10-01"


Profile: ACPOtherImportantInformation
Parent: Observation
Id: ACP-OtherImportantInformation
Title: "Other Important Information"
Description: "Other relevant and important information related to the Patient’s Advance Care Planning (ACP) agreements."
* insert MetaRules
* encounter only Reference(Encounter)
* subject only Reference(Patient)
* code = $snomed#247751003 // TODO -- check if snomed code 247751003 is correct: "Gevoel van zingeving (waarneembare entiteit)"
* value[x] only string
* value[x] ^definition = "Other relevant and important information related to the Patient’s Advance Care Planning (ACP) agreements."


Mapping: MapACPOtherImportantInformation
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPOtherImportantInformation
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "709" "Wat verder nog belangrijk is ([Meting])"
* code -> "710" "Wat verder nog belangrijk is ([MetingNaam])"
* valueString -> "711" "Wat verder nog belangrijk is ([MetingWaarde])"
* effective[x] -> "715" "[MeetDatumBeginTijd]"


Instance: F1-ACP-OtherImportantInformation
InstanceOf: ACPOtherImportantInformation
Title: "F1 ACP Other Important Information"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "eef80c58-5721-45fa-8f05-210f9e1f0b63"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#247751003
* valueString = "Michiel gaat nadenken over wat hij belangrijk vindt. Over een tijdje vervolggesprek"
* effectiveDateTime = "2020-10-01"






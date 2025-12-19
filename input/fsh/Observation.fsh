Profile: ACPSpecificCareWishes
Parent: Observation
Id: ACP-SpecificCareWishes
Title: "Specific Care Wishes"
Description: "The patient's wishes and expectations concerning their treatment, as an answer to the questions: 'What, according to the patient, should healthcare providers know to provide good care? Does this patient have specific wishes regarding their care (including cultural, religious, social, and spiritual aspects)?' Based on Observation resource."
* insert MetaRules

* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#153851000146100 
* value[x] only string
* dataAbsentReason ^comment = "The `dataAbsentReason` is helpful to indicate a more detailed reason on why the data is absent if this is known, namely: 
- if the question has been asked but the source does not know the value (code = _asked-unknown_) 
- if the question has not been asked (code = _not-asked_) "
* method = $snomed#370819000

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueString)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(method)
* insert ObligationRules(effective[x])  

Mapping: MapACPSpecificCareWishes
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPSpecificCareWishes
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "654" "Specifieke wensen ([Meting])"
* code -> "655" "Wens en verwachting patient ([MetingNaam])"
* valueString -> "656" "Wens en verwachting patient ([MetingWaarde])"
* dataAbsentReason -> "656" "Wens en verwachting patient ([MetingWaarde])"
* method -> "657" "Vaststellen wens en verwachting patiënt ([MeetMethode])"
* effective[x] -> "660" "[MeetDatumBeginTijd]"


Instance: F1-ACP-SpecificCareWishes
InstanceOf: ACPSpecificCareWishes
Title: "F1 ACP Specific Care Wishes"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c68d0feb-ee43-45d5-86f5-a7f43a20f167"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#153851000146100 "wensen en verwachtingen met betrekking tot uitkomst van behandeling"
* valueString = "Hendrik wil er alles aan doen om zo lang mogelijk in goede gezondheid te kunnen leven. Hij probeert regelmatig te sporten en zou graag willen blijven hardlopen. Broer Michiel woont om de hoek en is erg betrokken bij het proces van Hendrik"
* effectiveDateTime = "2020-10-01"
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg (verrichting)"


// In R5/build of FHIR at CarePlan this is noted: 
//  "Self-maintained patient or care-giver authored plans identifying their goals and an integrated understanding of actions to be taken. 
//  This does not include the legal Advance Directives, which should be represented with either the Consent resource with Consent.category = Advance Directive or with a specific request resource with intent = directive. 
//  Informal advance directives could be represented as a Goal, such as "I want to die at home."
// For future versions of the IG on R5/R6 onwards, we should consider using Goal instead of Observation. 
Profile: ACPPreferredPlaceOfDeath
Parent: Observation
Id: ACP-PreferredPlaceOfDeath
Title: "Preferred Place Of Death"
Description: "The preferred place of death. This is the place where the patient prefers to die, if possible. The preferred place of death can be a home, a hospital, a nursing home, hospice or another location. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#395091006 
* value[x] only CodeableConcept 
* value[x] from ACPPreferredPlaceOfDeathVS (extensible)

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueCodeableConcept)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])
* insert ObligationRules(note.text)

Mapping: MapACPSPreferredPlaceOfDeath
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPPreferredPlaceOfDeath
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "666" "Gewenste plek van overlijden ([Meting]))"
* code -> "667" "Gewenste plek van overlijden ([Meting])"
* valueCodeableConcept -> "668" "Voorkeursplek ([MetingWaarde])"
* dataAbsentReason -> "668" "Voorkeursplek ([MetingWaarde])"
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
* code =  $snomed#395091006 "Preferred place of death"
// * valueCodeableConcept = $v3-NullFlavor#UNK  -- Cannot have a value[x] if you have data absent reason
* dataAbsentReason = $DataAbsentReason#asked-unknown 
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"


Profile: ACPPositionRegardingEuthanasia
Parent: Observation
Id: ACP-PositionRegardingEuthanasia
Title: "Position Regarding Euthanasia"
Description: "The patient's position regarding euthanasia. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#340171000146104 
* value[x] only CodeableConcept
* value[x] ^definition = "Position regarding euthanesia."
* value[x] from ACPEuthanasiaStatementVS (required)
* note.text ^definition = "Comment accompanying position regarding euthanesia."

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueCodeableConcept)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])
* insert ObligationRules(note.text)


Mapping: MapACPPositionRegardingEuthanasia
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPPositionRegardingEuthanasia
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "678" "Euthanasie standpunt ([Meting])"
* code -> "679" "Euthanasie standpunt ([MetingNaam])"
* valueCodeableConcept -> "680" "Euthanasie standpunt ([MetingWaarde])"
* dataAbsentReason -> "680" "Euthanasie standpunt ([MetingWaarde])"
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
* code =  $snomed#340171000146104 "standpunt ten opzichte van euthanasie"
* valueCodeableConcept = $v3-NullFlavor#UNK
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"


Profile: ACPOrganDonationChoiceRegistration
Parent: Observation
Id: ACP-OrganDonationChoiceRegistration
Title: "Organ donation choice registration in donor register"
Description: "Answer, captured in an observation, to the question: 'Is the choice on organ donation recorded in the donor register?' Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#570801000146104
* value[x] only CodeableConcept
* value[x] ^definition = "Organ donation choice recorded in donor register."
* value[x] from ACPYesNoUnknownVS (required)

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueCodeableConcept)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])  

Mapping: MapACPOrganDonationChoiceRegistration
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPOrganDonationChoiceRegistration
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "746" "Keuze orgaandonatie vastgelegd in donorregister? ([Meting])"
* code -> "747" "Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam])"
* valueCodeableConcept -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
* dataAbsentReason -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
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
* code = $snomed#570801000146104 "geregistreerd in orgaan donorregister"
* valueCodeableConcept = $snomed#373066001 "ja"
* effectiveDateTime = "2020-10-01"


Profile: ACPSenseOfPurpose
Parent: Observation
Id: ACP-SenseOfPurpose
Title: "Sense of Purpose"
Description: "Observation capturing the patient's sense of purpose and other important information in the context of Advance Care Planning. While the primary concept is 'sense of purpose' (SNOMED 247751003), this profile serves as a container in the ACP dataset for capturing additional relevant information that may influence care decisions. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#247751003 // SNOMED code 247751003 may seem strange but is agreed upon by experts.
* value[x] only string
* value[x] ^definition = "Other relevant and important information related to the Patient’s Advance Care Planning (ACP) agreements."

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueString)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])


Mapping: MapACPSenseOfPurpose
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPSenseOfPurpose
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "709" "Wat verder nog belangrijk is ([Meting])"
* code -> "710" "Wat verder nog belangrijk is ([MetingNaam])"
* valueString -> "711" "Wat verder nog belangrijk is ([MetingWaarde])"
* dataAbsentReason -> "711" "Wat verder nog belangrijk is ([MetingWaarde])"
* effective[x] -> "715" "[MeetDatumBeginTijd]"



Instance: F1-ACP-ACPSenseOfPurpose
InstanceOf: ACPSenseOfPurpose
Title: "F1 ACP Sense of Purpose"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "eef80c58-5721-45fa-8f05-210f9e1f0b63"
* encounter = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* performer = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#247751003 "gevoel van zingeving" // Sense of purpose (observable entity)
* valueString = "Michiel gaat nadenken over wat hij belangrijk vindt. Over een tijdje vervolggesprek"
* effectiveDateTime = "2020-10-01"
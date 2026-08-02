Profile: ACPSpecificCareWishes
Parent: Observation
Id: ACP-SpecificCareWishes
Title: "ACP Specific Care Wishes"
Description: "The patient's wishes and expectations concerning their treatment, as an answer to the questions: 'What, according to the patient, should healthcare providers know to provide good care? Does this patient have specific wishes regarding their care (including cultural, religious, social, and spiritual aspects)?' Based on Observation resource."
* insert MetaRules

* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#153851000146100 
* value[x] only string
* dataAbsentReason ^comment = "The `dataAbsentReason` is helpful to indicate a more detailed reason on why the data is absent if this is known, namely: 
- if the question has been asked but the source does not know the value (code = _asked-unknown_) 
- if the question has not been asked (code = _not-asked_) "
* method 1..1
* method = $snomed#370819000

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueString)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(method)
* insert ObligationRules(effective[x])  
* insert ObligationRules(performer)

Mapping: MapACPSpecificCareWishes
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPSpecificCareWishes
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "654" "Specifieke wensen ([Meting])"
* code -> "655" "Wens en verwachting patient ([MetingNaam])"
* valueString -> "656" "Wens en verwachting patient ([MetingWaarde])"
* dataAbsentReason -> "656" "Wens en verwachting patient ([MetingWaarde])"
* method -> "657" "Vaststellen wens en verwachting patiënt ([MeetMethode])"
* effective[x] -> "660" "[MeetDatumBeginTijd]"


Instance: ACP-SpecificCareWishes-Pat1
InstanceOf: ACPSpecificCareWishes
Title: "ACP Specific Care Wishes - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c68d0feb-ee43-45d5-86f5-a7f43a20f167"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#153851000146100 "wensen en verwachtingen met betrekking tot uitkomst van behandeling"
* valueString = "Hendrik wil er alles aan doen om zo lang mogelijk in goede gezondheid te kunnen leven. Hij probeert regelmatig te sporten en zou graag willen blijven hardlopen. Broer Michiel woont om de hoek en is erg betrokken bij het proces van Hendrik"
* effectiveDateTime = "2020-10-01"
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg (verrichting)"


Instance: ACP-SpecificCareWishes-Pat2
InstanceOf: ACPSpecificCareWishes
Title: "ACP Specific Care Wishes - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "171c806c-a4bf-4b1e-a7d4-497e9ed44278"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#153851000146100 "wensen en verwachtingen met betrekking tot uitkomst van behandeling"
* valueString = "De kleinzoon van mevrouw van der Sluijs is geboren en mevrouw is dolgelukkig dat ze hem heeft kunnen zien. Ze merkt dat ze fysiek erg achteruitgaat. Mevrouw heeft daar nu vrede mee, in tegenstelling tot eerdere gesprekken."
* effectiveDateTime = "2025-08-07"
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg"


// In R5/build of FHIR at CarePlan this is noted: 
//  "Self-maintained patient or care-giver authored plans identifying their goals and an integrated understanding of actions to be taken. 
//  This does not include the legal Advance Directives, which should be represented with either the Consent resource with Consent.category = Advance Directive or with a specific request resource with intent = directive. 
//  Informal advance directives could be represented as a Goal, such as "I want to die at home."
// For future versions of the IG on R5/R6 onwards, we should consider using Goal instead of Observation. 
Profile: ACPPreferredPlaceOfDeath
Parent: Observation
Id: ACP-PreferredPlaceOfDeath
Title: "ACP Preferred Place of Death"
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
* insert ObligationRules(performer)

Mapping: MapACPSPreferredPlaceOfDeath
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPPreferredPlaceOfDeath
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "666" "Gewenste plek van overlijden ([Meting]))"
* code -> "667" "Gewenste plek van overlijden ([Meting])"
* valueCodeableConcept -> "668" "Voorkeursplek ([MetingWaarde])"
* dataAbsentReason -> "668" "Voorkeursplek ([MetingWaarde])"
* effective[x] -> "672" "[MeetDatumBeginTijd]"
* note.text -> "674" "[Toelichting]"


Instance: ACP-PreferredPlaceOfDeath-Pat1
InstanceOf: ACPPreferredPlaceOfDeath
Title: "ACP Preferred Place of Death - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "023ba125-94c3-492c-8379-958ac9fbb9d6"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#395091006 "gewenste plek van overlijden"
// * valueCodeableConcept = $v3-NullFlavor#UNK  -- Cannot have a value[x] if you have data absent reason
* dataAbsentReason = $DataAbsentReason#asked-unknown 
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"


Instance: ACP-PreferredPlaceOfDeath-Pat2
InstanceOf: ACPPreferredPlaceOfDeath
Title: "ACP Preferred Place of Death - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d1866b00-aa64-4155-aa20-25ce51dac894"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#395091006 "gewenste plek van overlijden"
* effectiveDateTime = "2025-08-07"
* valueCodeableConcept = $v3-NullFlavor#OTH "Anders"
* valueCodeableConcept.text = "bijna-thuis-huis"
* note.text = "Het liefst in een bijna-thuis-huis in de buurt van haar kinderen"


Profile: ACPPositionRegardingEuthanasia
Parent: Observation
Id: ACP-PositionRegardingEuthanasia
Title: "ACP Position Regarding Euthanasia"
Description: "The patient's position regarding euthanasia. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#340171000146104
* value[x] only CodeableConcept
* value[x] ^definition = "Position regarding euthanasia."
* value[x] from ACPPositionRegardingEuthanasiaVS (required)
* note.text ^definition = "Comment accompanying position regarding euthanasia."

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueCodeableConcept)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])
* insert ObligationRules(note.text)
* insert ObligationRules(performer)


Mapping: MapACPPositionRegardingEuthanasia
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPPositionRegardingEuthanasia
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "678" "Euthanasie standpunt ([Meting])"
* code -> "679" "Euthanasie standpunt ([MetingNaam])"
* valueCodeableConcept -> "680" "Euthanasie standpunt ([MetingWaarde])"
* dataAbsentReason -> "680" "Euthanasie standpunt ([MetingWaarde])"
* effective[x] -> "684" "[MeetDatumBeginTijd]"
* note.text -> "686" "[Toelichting]"


Instance: ACP-PositionRegardingEuthanasia-Pat1
InstanceOf: ACPPositionRegardingEuthanasia
Title: "ACP Position Regarding Euthanasia - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f2314b60-1b52-4f29-b231-8b74869fc34b"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#340171000146104 "standpunt ten opzichte van euthanasie"
* valueCodeableConcept = $v3-NullFlavor#UNK
* effectiveDateTime = "2020-10-01"
* note.text = "Nog niet besproken"


Instance: ACP-PositionRegardingEuthanasia-Pat2
InstanceOf: ACPPositionRegardingEuthanasia
Title: "ACP Position Regarding Euthanasia - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "1e73ad4f-6822-412e-a8e1-8a9f235e5a54"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#340171000146104 "standpunt ten opzichte van euthanasie"
* valueCodeableConcept = $snomed#340201000146103 "wil geen euthanasie"
* effectiveDateTime = "2025-08-07"


Profile: ACPOrganDonationChoiceRegistration
Parent: Observation
Id: ACP-OrganDonationChoiceRegistration
Title: "ACP Organ Donation Choice Registration in Donor Register"
Description: "Observation capturing whether the patient's organ donation choice is recorded in the donor register as reported by the patient. It is intended to track the administrative status of the decision rather than the clinical or legal specifics of the donation choice itself. This information is exchanged so the next caregiver knows whether the topic requires attention in future ACP conversations. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#570801000146104
* method 1..1
* method = $snomed#1156040003
* value[x] only CodeableConcept
* value[x] ^definition = "Organ donation choice recorded in donor register."
* value[x] from ACPYesNoUnknownVS (required)

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(method)
* insert ObligationRules(valueCodeableConcept)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x]) 
* insert ObligationRules(performer) 

Mapping: MapACPOrganDonationChoiceRegistration
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPOrganDonationChoiceRegistration
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "746" "Keuze orgaandonatie vastgelegd in donorregister? ([Meting])"
* code -> "747" "Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam])"
* valueCodeableConcept -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
* dataAbsentReason -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
* effective[x] -> "752" "[MeetDatumBeginTijd]"


Instance: ACP-OrganDonationChoiceRegistration-Pat1
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "ACP Organ Donation Choice Registration in Donor Register - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "31952dca-757c-4e4e-b7f6-fab66a79deba"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code = $snomed#570801000146104 "geregistreerd in orgaan donorregister"
* method = $snomed#1156040003 "self reported"
* valueCodeableConcept = $snomed#373066001 "ja"
* effectiveDateTime = "2020-10-01"


Instance: ACP-OrganDonationChoiceRegistrationInDonorRegister-Pat2
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "ACP Organ Donation Choice Registration in Donor Register - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "856791c1-91cf-404a-ab2e-e1ed05c7c880"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#570801000146104 "geregistreerd in orgaan donorregister"
* method = $snomed#1156040003 "self reported"
* valueCodeableConcept = $snomed#373066001 "ja"
* effectiveDateTime = "2025-08-07"


Profile: ACPSenseOfPurpose
Parent: Observation
Id: ACP-SenseOfPurpose
Title: "ACP Sense of Purpose"
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
* insert ObligationRules(performer)


Mapping: MapACPSenseOfPurpose
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPSenseOfPurpose
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07%3A58%3A08"
* -> "709" "Wat verder nog belangrijk is ([Meting])"
* code -> "710" "Wat verder nog belangrijk is ([MetingNaam])"
* valueString -> "711" "Wat verder nog belangrijk is ([MetingWaarde])"
* dataAbsentReason -> "711" "Wat verder nog belangrijk is ([MetingWaarde])"
* effective[x] -> "715" "[MeetDatumBeginTijd]"


Instance: ACP-SenseOfPurpose-Pat1
InstanceOf: ACPSenseOfPurpose
Title: "ACP Sense of Purpose - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "eef80c58-5721-45fa-8f05-210f9e1f0b63"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#247751003 "gevoel van zingeving" // Sense of purpose (observable entity)
* valueString = "Hendrik gaat nadenken over wat hij belangrijk vindt. Over een tijdje vervolggesprek"
* effectiveDateTime = "2020-10-01"


Instance: ACP-SenseOfPurpose-Pat2
InstanceOf: ACPSenseOfPurpose
Title: "ACP Sense Of Purpose - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "45ff425e-5c09-4930-b4ea-3819dc857734"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#247751003 "gevoel van zingeving"
* valueString = "Mevrouw is gek op haar kleinzoon, dus brengt graag veel tijd met hem door."
* effectiveDateTime = "2025-08-07"


Profile: ACPLegallyCapable
Parent: Observation
Id: ACP-LegallyCapable
Title: "ACP Legally Capable"
Description: "Indicates whether the patient is currently assessed as having the capacity to understand and oversee the consequences of medical treatment decisions. If the patient is not legally capable, there should be a legal representative captured in a RelatedPerson resource. Based on Observation resource."
* insert MetaRules
* encounter only Reference(ACPEncounter)
* subject only Reference(ACPPatient)
* code = $snomed#665671000146101
* value[x] only boolean

* insert ObligationRules(encounter)
* insert ObligationRules(subject)
* insert ObligationRules(code)
* insert ObligationRules(valueBoolean)
* insert ObligationRules(dataAbsentReason)
* insert ObligationRules(effective[x])
* insert ObligationRules(note.text)
* insert ObligationRules(performer)

Mapping: MapACPLegallyCapable
Id: pall-izppz-zib2020
Title: "ACP dataset"
Source: ACPLegallyCapable
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-02-24T09:29:59"
* -> "761" "Wilsbekwaamheid m.b.t. medische behandelbeslissingen"
* valueBoolean -> "762" "Wilsbekwaamheid m.b.t. medische behandelbeslissingen"
* dataAbsentReason -> "762" "Wilsbekwaamheid m.b.t. medische behandelbeslissingen"
* note.text -> "763" "[Toelichting]"


Instance: ACP-LegallyCapable-Pat1
InstanceOf: ACPLegallyCapable
Title: "ACP Legally Capable - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "928e493b-3265-46ad-a155-b46d3d31b821"
* encounter = Reference(ACP-Encounter-Pat1) "Encounter, 2020-10-01"
* subject = Reference(ACP-Patient-HendrikHartman-Pat1) "Patient, Hendrik Hartman"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1) "Healthcare professional (role), van Huissen"
* status = #final
* code =  $snomed#665671000146101 "juridisch in staat om beslissingen te nemen over medische behandelingen"
* valueBoolean = true
* effectiveDateTime = "2020-10-01"


Instance: ACP-LegallyCapable-Pat2
InstanceOf: ACPLegallyCapable
Title: "ACP Legally Capable - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "337d9e4a-08a3-486f-9f24-d6c60c6f342a"
* encounter = Reference(ACP-Encounter-1-Pat2) "Encounter, 2025-08-07"
* subject = Reference(ACP-Patient-SamiraVanDerSluijs-Pat2) "Patient, Samira van der Sluijs"
* performer = Reference(ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#665671000146101 "juridisch in staat om beslissingen te nemen over medische behandelingen"
* valueBoolean = true
* effectiveDateTime = "2025-08-07"
* note.text = "Patiënt is wilsbekwaam. Bij verandering van de situatie wordt haar partner haar wettelijk vertegenwoordiger."
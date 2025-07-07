Profile: ACPSpecificCareWishes
Parent: Observation
Id: ACP-SpecificCareWishes
Title: "ACP Specific Care Wishes"
Description: "What, according to the patient, should healthcare providers know to provide good care? Does this patient have specific wishes regarding their care (including cultural, religious, social, and spiritual aspects)? The patient's wishes and expectations concerning their treatment, based on the [Measurement] building block"
* insert MetaRules
* code = $snomed#153851000146100 // TODO -- check if there is a international code for this?
* value[x] only string
* method = $snomed#370819000 // TODO -- check if we want this code to be present and if it actually maps to Observation.method Display: "Vaststellen van persoonlijke waarden en wensen met betrekking tot zorg" 

Mapping: MapACPSpecificCareWishes
Id: pall-izppz-v2025-03-11
Title: "Specifieke wensen ([Meting])"
Source: ACPSpecificCareWishes
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "391" "Specifieke wensen ([Meting])"
* code -> "655" "Wens en verwachting patient ([MetingNaam])"
* valueString -> "656" "Wens en verwachting patient ([MetingWaarde])"
* method -> "657" "Vaststellen wens en verwachting patiënt ([MeetMethode])"
* effective[x] -> "660" "[MeetDatumBeginTijd]"


Profile: ACPPreferredPlaceOfDeath
Parent: Observation
Id: ACP-PreferredPlaceOfDeath
Title: "ACP Preferred Place Of Death"
Description: "The preferred place of death as recorded in the ACP form. This is the place where the patient prefers to die, if possible. The preferred place of death can be a home, a hospital, a nursing home, or another location."
* insert MetaRules
* code = $snomed#395091006 
* value[x] only CodeableConcept 
* value[x] from ACPPreferredPlaceOfDeathVS (extensible) // TODO - there is no binding strenght in dataset.



Mapping: MapACPSPreferredPlaceOfDeath
Id: pall-izppz-v2025-03-11
Title: "Gewenste plek van overlijden ([Meting])"
Source: ACPPreferredPlaceOfDeath
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "666" "Gewenste plek van overlijden ([Meting]))"
* code -> "667" "Gewenste plek van overlijden ([Meting])"
* valueCodeableConcept -> "656" "Wens en verwachting patient ([MetingWaarde])"
* effective[x] -> "672" "[MeetDatumBeginTijd]"
* note.text -> "674" "[Toelichting]"



Profile: ACPPositionRegardingEuthanasia
Parent: Observation
Id: ACP-PositionRegardingEuthanasia
Title: "ACP Position Regarding Euthanasia"
Description: "Position Regarding Euthanasia"
* insert MetaRules
* code = $snomed#340171000146104 // TODO -- check if there is a international code for this?
* value[x] only CodeableConcept
* value[x] ^definition = "Response to the question “Position regarding euthanesia” as recorded in the ACP form."
* value[x] from ACPEuthanasiaStatementVS (extensible) // TODO - there is no binding strenght in dataset.
* note.text ^short = "Comment, Toelichting"
* note.text ^definition = "Comment accompanying the response to the question “Position regarding euthanesia” as recorded in the ACP form."

Mapping: MapACPPositionRegardingEuthanasia
Id: pall-izppz-v2025-03-11
Title: "Euthanasie standpunt ([Meting])"
Source: ACPPositionRegardingEuthanasia
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "678" "Euthanasie standpunt ([Meting])"
* code -> "679" "Euthanasie standpunt ([MetingNaam])"
* valueCodeableConcept -> "680" "Euthanasie standpunt ([MetingWaarde])"
* effective[x] -> "684" "[MeetDatumBeginTijd]"
* note.text -> "686" "[Toelichting]"


Profile: ACPDonorRegistration
Parent: Observation
Id: ACP-DonorRegistration
Title: "ACP Donor Registration"
Description: "Donor Registration"
* insert MetaRules
* code = $snomed#TODO // TODO -- no code in dataset?
* value[x] only CodeableConcept
* value[x] ^definition = "Response to the question “Donor Registration” as recorded in the ACP form."
* value[x] from ACPYesNoUnknownVS (required) // TODO - there is no binding strenght in dataset.

Mapping: MapACPDonorRegistration
Id: pall-izppz-v2025-03-11
Title: "Keuze orgaandonatie vastgelegd in donorregister? ([Meting])"
Source: ACPDonorRegistration
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "746" "Keuze orgaandonatie vastgelegd in donorregister? ([Meting])"
* code -> "747" "Keuze orgaandonatie vastgelegd in donorregister? ([MetingNaam])"
* valueCodeableConcept -> "748" "Keuze orgaandonatie in donorregister ([MetingWaarde])"
* effective[x] -> "752" "[MeetDatumBeginTijd]"





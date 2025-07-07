Profile: ACPAdvanceDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-AdvanceDirective
Id: ACP-AdvanceDirective
Title: "ACP AdvanceDirective"
Description: "A living will is a verbal or written description of the patient’s wishes with regard to future medical action or end of their life. A living will is mainly used for situations in which the patient is no longer able to speak about these decisions with their healthcare provider."
* insert MetaRules
* provision.code ^comment = " The following codes are in scope of this profile:
- For Euthanasia, either codes EU (Euthanasieverzoek) or EUD (Euthanasieverzoek met aanvulling Dementie).
- For Organ Donation, the code is DO (Verklaring donorschap)." //TODO discuss if we need a custom profile or not.
Mapping: MapACPAdvanceDirective
Id: pall-izppz-v2025-03-11
Title: "Euthanasieverklaring (Wilsverklaring) / Keuze orgaandonatie vastgelegd (Wilsverklaring) "
Source: ACPAdvanceDirective
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "690" "Euthanasieverklaring (Wilsverklaring)"
* -> "700" "Keuze orgaandonatie vastgelegd (Wilsverklaring)"
* extension[comment].value[x] -> "698" "Toelichting"
* extension[comment].value[x] -> "708" "Toelichting"
* extension[disorder] -> "693" "Aandoening"
* extension[disorder] -> "703" "Aandoening"
* dateTime -> "692" "WilsverklaringDatum"
* dateTime -> "702" "WilsverklaringDatum"
* sourceAttachment -> "697" "WilsverklaringDocument" // Is 0..1 in dataset, so we don't need the extension :) 
* sourceAttachment -> "707" "WilsverklaringDocument" // Is 0..1 in dataset, so we don't need the extension :) 
* provision.actor[representative].reference -> "693" "Vertegenwoordiger"
* provision.actor[representative].reference -> "705" "Vertegenwoordiger"
* provision.code -> "691" "Euthanasieverklaring (WilsverklaringType)"
* provision.code -> "701" "Euthanasieverklaring (WilsverklaringType)"




Profile: ACPTreatmentDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-TreatmentDirective2
Id: ACP-TreatmentDirective
Title: "ACP TreatmentDirective"
Description: "A treatment directive contains a joint decision between a health professional (for example a general practitioner) and a patient or his representative(s) about the desirability of performing a certain treatment, such as resuscitation, before this treatment becomes (acute) necessary."
* insert MetaRules


Mapping: MapACPTreatmentDirective
Id: pall-izppz-v2025-03-11
Title: "Behandelgrens (BehandelAanwijzing)"
Source: ACPTreatmentDirective
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "602" "Behandelgrens (BehandelAanwijzing)"
* modifierExtension[specificationOther] -> "605" "SpecificatieAnders"
* extension[comment].value[x] -> "618" "Toelichting"
* dateTime -> "606" "MeestRecenteBespreekdatum"
* sourceReference -> "609" "Wilsverklaring"
* provision.type -> "603" "BehandelBesluit"
* provision.extension[reasonForEnding] -> "608" "RedenBeeindigd"
* provision.period.end -> "607" "DatumBeeindigd"
* provision.actor[agreementParty] -> "611" "AfspraakPartij"
* provision.actor[agreementParty].reference -> "612" "Patient"
* provision.actor[agreementParty].reference -> "614" "Vertegenwoordiger"
* provision.actor[agreementParty].reference -> "616" "Zorgverlener"
* provision.code -> "604" "Behandeling"


Profile: ACPTreatmentDirectiveICD
Parent: ACPTreatmentDirective
Id: ACP-TreatmentDirective-ICD
Title: "ACP TreatmentDirective ICD"
Description: "A treatment directive regarding a ICD."
* insert MetaRules
* provision.type ^comment = "BehandelBesluit values yes = permit, no = deny or unknown. If unknown, then the value is not set." //TODO check if we want a ConceptMap? 
* provision.code from ACPTreatmentDirectiveICDVS (required)

Mapping: MapACPTreatmentDirectiveICD
Id: pall-izppz-v2025-03-11-2 //TODO check, here we suffixed the mapping identifier with -2, because the mapping identifier is already used in the previous mapping.
Title: "Afspraak uitzetten ICD (BehandelAanwijzing)"
Source: ACPTreatmentDirectiveICD
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "637" "Behandelgrens (BehandelAanwijzing)"
// TODO specification other -> "605" "SpecificatieAnders"
// TODO SpecificationOther is not in the dataset here! But is needed because Afspraak uitzetten ICD contains, yes, no and onbekend.
* extension[comment].value[x] -> "618" "Toelichting"
* dateTime -> "641" "MeestRecenteBespreekdatum"
* sourceReference -> "644" "Wilsverklaring"
* provision.type -> "638" "Afspraak uitzetten ICD (BehandelBesluit)"
* provision.extension[reasonForEnding] -> "643" "RedenBeeindigd"
* provision.period.end -> "642" "DatumBeeindigd"
* provision.actor[agreementParty] -> "646" "AfspraakPartij"
* provision.actor[agreementParty].reference -> "647" "Patient"
* provision.actor[agreementParty].reference -> "649" "Vertegenwoordiger"
* provision.actor[agreementParty].reference -> "651" "Zorgverlener"
* provision.code -> "604" "Behandeling van ICD (Behandeling)"


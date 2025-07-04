Profile: ACPAdvanceDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-AdvanceDirective
Id: ACP-AdvanceDirective
Title: "ACP AdvanceDirective"
Description: "[TO-DO]"
* insert MetaRules




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
// TODO -> "608" "RedenBeeindigd"
// TODO specification other -> "605" "SpecificatieAnders"
* extension[comment].value[x] -> "618" "Toelichting"
* dateTime -> "606" "MeestRecenteBespreekdatum"
* sourceReference -> "609" "Wilsverklaring"
* provision.type -> "603" "BehandelBesluit"
* provision.period.end -> "607" "DatumBeeindigd"
* provision.actor[agreementParty] -> "611" "AfspraakPartij"
* provision.actor[agreementParty].reference -> "612" "Patient"
* provision.actor[agreementParty].reference -> "614" "Vertegenwoordiger"
* provision.actor[agreementParty].reference -> "616" "Zorgverlener"
* provision.code -> "604" "Behandeling"

Profile: ACPAdvanceDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-AdvanceDirective
Id: ACP-AdvanceDirective
Title: "AdvanceDirective"
Description: "A living will is a verbal or written description of the patient’s wishes with regard to future medical action or end of their life. A living will is mainly used for situations in which the patient is no longer able to speak about these decisions with their healthcare provider."
* insert MetaRules
* provision.code ^comment = " The following codes are in scope of this profile:
- For Euthanasia, either codes EU (Euthanasieverzoek) or EUD (Euthanasieverzoek met aanvulling Dementie).
- For Organ Donation, the code is DO (Verklaring donorschap)." //TODO discuss if we need a custom profile or not.
* patient only Reference(ACPPatient)

Mapping: MapACPAdvanceDirective
Id: pall-izppz-v2025-03-11
Title: "Euthanasieverklaring (Wilsverklaring) / Keuze orgaandonatie vastgelegd (Wilsverklaring) / Eerder vastgelegde behandelafspraken (Wilsverklaring)"
Source: ACPAdvanceDirective
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "690" "Euthanasieverklaring (Wilsverklaring)"
* -> "700" "Keuze orgaandonatie vastgelegd (Wilsverklaring)"
* -> "721" "Eerder vastgelegde behandelafspraken (Wilsverklaring)"
* extension[comment].value[x] -> "698" "Toelichting"
* extension[comment].value[x] -> "708" "Toelichting"
* extension[comment].value[x] -> "729" "Toelichting"
* extension[disorder] -> "693" "Aandoening"
* extension[disorder] -> "703" "Aandoening"
* extension[disorder] -> "724" "Aandoening"
* dateTime -> "692" "WilsverklaringDatum"
* dateTime -> "702" "WilsverklaringDatum"
* dateTime -> "723" "WilsverklaringDatum"
* sourceAttachment -> "697" "WilsverklaringDocument" // Is 0..1 in dataset, so we don't need the extension, but better leave it be? :) 
* sourceAttachment -> "707" "WilsverklaringDocument" // Is 0..1 in dataset, so we don't need the extension, but better leave it be? :) 
* sourceAttachment -> "728" "WilsverklaringDocument" // Is 0..1 in dataset, so we don't need the extension, but better leave it be? :) 
* provision.actor[representative].reference -> "693" "Vertegenwoordiger"
* provision.actor[representative].reference -> "705" "Vertegenwoordiger"
* provision.actor[representative].reference -> "705" "Vertegenwoordiger"
* provision.code -> "691" "Euthanasieverklaring (WilsverklaringType)"
* provision.code -> "701" "Orgaandonatie (WilsverklaringType)"
* provision.code -> "722" "WilsverklaringType"

Profile: ACPTreatmentDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-TreatmentDirective2
Id: ACP-TreatmentDirective
Title: "TreatmentDirective"
Description: "A treatment directive contains a joint decision between a health professional (for example a general practitioner) and a patient or his representative(s) about the desirability of performing a certain treatment, such as resuscitation, before this treatment becomes (acute) necessary."
* insert MetaRules
* patient only Reference(ACPPatient)

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
Title: "TreatmentDirective ICD"
Description: "A treatment directive regarding a ICD."
* insert MetaRules
* patient only Reference(ACPPatient)
* provision.type ^comment = "BehandelBesluit values yes = permit, no = deny or unknown. If unknown, then the value is not set." //TODO check if we want a ConceptMap? 
* provision.code from ACPTreatmentDirectiveICDVS (required) // TODO this is not valid to do because of required binding

Mapping: MapACPTreatmentDirectiveICD
Id: pall-izppz-v2025-03-11-2 //TODO check, here we suffixed the mapping identifier with -2, because the mapping identifier is already used in the previous mapping.
Title: "Afspraak uitzetten ICD (BehandelAanwijzing)"
Source: ACPTreatmentDirectiveICD
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "637" "Afspraak uitzetten ICD (BehandelAanwijzing)"
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
* provision.code -> "639" "Behandeling van ICD (Behandeling)" //TODO check if this matches the binding strength of zib, which is required. 



Instance: F1-ACP-TreatmentDirective-305351004
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 305351004"
Usage: #example
// TODO: add an identifier too? For showing good practice.
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#305351004 "opname op intensive care"

Instance: F1-ACP-TreatmentDirective-89666000
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 89666000"
Usage: #example
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty].reference.type = "PractitionerRole"
* provision.code = $snomed#89666000 "cardiopulmonale resuscitatie"

Instance: F1-ACP-TreatmentDirective-40617009
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 40617009"
Usage: #example
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#40617009 "kunstmatige beademing"

Instance: F1-ACP-TreatmentDirective-116762002
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 116762002"
Usage: #example
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#116762002 "toediening van bloedproduct"

Instance: F1-ACP-TreatmentDirective-281789004
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 281789004"
Usage: #example
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#281789004 "antibiotische therapie"

Instance: F1-ACP-TreatmentDirective-32485007
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 32485007"
Usage: #example
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#32485007 "opname in ziekenhuis"

Instance: F1-ACP-TreatmentDirective-400231000146108
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective ICD"
Usage: #example
* modifierExtension[specificationOther].valueString = "Niet besproken" // TODO check if this is ok...
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* status = #active
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $v3-NullFlavor#OTH
* provision.code.text = "Uitzetten van cardioverter-defibrillator in laatste levensfase (verrichting) (SNOMED CT - 400231000146108)" // TODO check if this is ok.

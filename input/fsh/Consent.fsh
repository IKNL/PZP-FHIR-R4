Profile: ACPAdvanceDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-AdvanceDirective
Id: ACP-AdvanceDirective
Title: "AdvanceDirective"
Description: "A verbal or written description of the patient’s wishes with regard to future medical action or end of their life. A living will is mainly used for situations in which the patient is no longer able to speak about these decisions with their healthcare provider. Based on nl-core-AdvanceDirective and HCIM AdvanceDirective."
* insert MetaRules
* extension contains
    ExtEncounterReference  named encounter 0..1
* extension[encounter].valueReference only Reference(ACPEncounter) 
* provision.code ^definition = " The following codes are in scope of this profile:
- For Euthanasia, codes _EU_ (Euthanasieverzoek) or _EUD_ (Euthanasieverzoek met aanvulling Dementie).
- For Organ Donation, code _DO_ (Verklaring donorschap)."
// Why not NR?
* patient only Reference(ACPPatient)


Mapping: MapACPAdvanceDirective
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPAdvanceDirective
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "690" "Euthanasieverklaring (Wilsverklaring)"
* -> "700" "Keuze orgaandonatie vastgelegd (Wilsverklaring)"
* -> "721" "Eerder vastgelegde behandelafspraken (Wilsverklaring)"
* -> "610" "Wilsverklaring"
* -> "645" "Wilsverklaring"
* extension[comment].value[x] -> "698" "Toelichting"
* extension[comment].value[x] -> "708" "Toelichting"
* extension[comment].value[x] -> "729" "Toelichting"
* extension[disorder].value[x]  -> "693" "Aandoening"
* extension[disorder].value[x]  -> "703" "Aandoening"
* extension[disorder].value[x]  -> "724" "Aandoening"
* dateTime -> "692" "WilsverklaringDatum"
* dateTime -> "702" "WilsverklaringDatum"
* dateTime -> "723" "WilsverklaringDatum"
* sourceAttachment -> "697" "WilsverklaringDocument"   
* sourceAttachment -> "707" "WilsverklaringDocument"   
* sourceAttachment -> "728" "WilsverklaringDocument"   
* provision.actor[representative].reference -> "695" "Vertegenwoordiger"
* provision.actor[representative].reference -> "705" "Vertegenwoordiger"
* provision.actor[representative].reference -> "726" "Vertegenwoordiger"
* provision.code -> "691" "Euthanasieverklaring (WilsverklaringType)"
* provision.code -> "701" "Orgaandonatie (WilsverklaringType)"
* provision.code -> "722" "WilsverklaringType"


Profile: ACPTreatmentDirective
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-TreatmentDirective2
Id: ACP-TreatmentDirective
Title: "TreatmentDirective"
Description: "A joint decision between a health professional (for example a general practitioner) and a patient or his representative(s) about the desirability of performing a certain treatment, such as resuscitation, before this treatment becomes (acute) necessary. Based on nl-core-TreatmentDirective2 and HCIM TreatmentDirective2."
* insert MetaRules
* extension contains
    ExtEncounterReference  named encounter 0..1
* extension[encounter].valueReference only Reference(ACPEncounter) 
* extension[additionalAdvanceDirective].valueReference only Reference(ACPAdvanceDirective)
* modifierExtension[specificationOther].value[x] ^comment = "In addition to the default zib/nl-core guidance, this extension is used to communicate further details about agreements concerning ICD."
* patient only Reference(ACPPatient)
* source[x][sourceReference] only Reference(ACPAdvanceDirective)
* provision.type ^comment = "Additional terminology mapping guidance, in addition to the default zib/nl-core guidance: 
- BehandelBesluit (dataset id 603) values: 
    - _Ja_ -> _permit_
    - _Nee_ -> _deny_
    - _Ja maar met beperkingen_ or _Onbekend_ -> do not set a value. Instead, communicate this via the `modifierExtension[specificationOther].value[x]` element.
- Afspraak uitzetten ICD (dataset id 638) values: 
    - _Wel uitvoeren_ -> _permit_ 
    - No value is mapped to _deny_
    - _Nee, nog geen besluit genomen_ or _Niet besproken_ -> do not set a value. Instead, communicate this via the `modifierExtension[specificationOther].value[x]` element." 
* provision.code.text ^comment = "`.provision.type` has a required binding. Therefore, only codes in the bound ValueSet are permitted. For concepts not present in the ValueSet, such as SNOMED CT code 400231000146108 (Uitzetten van cardioverter-defibrillator in laatste levensfase), use the `.text` field as per FHIR guidance."
* provision.actor[agreementParty].reference only Reference(ACPPatient or ACPHealthProfessionalPractitionerRole or ACPContactPerson)


Mapping: MapACPTreatmentDirective
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPTreatmentDirective
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "602" "Behandelgrens (BehandelAanwijzing)"
* -> "637" "Afspraak uitzetten ICD (BehandelAanwijzing)"
* modifierExtension[specificationOther].value[x]  -> "605" "SpecificatieAnders"
* modifierExtension[specificationOther].value[x]  -> "638" "Afspraak uitzetten ICD (BehandelBesluit)"
* extension[comment].value[x] -> "618" "Toelichting"
* extension[comment].value[x] -> "653" "Toelichting"
* extension[additionalAdvanceDirective].valueReference -> "644" "Wilsverklaring"
* dateTime -> "606" "MeestRecenteBespreekdatum"
* sourceReference -> "609" "Wilsverklaring"
* provision.type -> "603" "BehandelBesluit"
* provision.extension[reasonForEnding].value[x]  -> "608" "RedenBeeindigd"
* provision.period.end -> "607" "DatumBeeindigd"
* provision.actor[agreementParty] -> "611" "AfspraakPartij"
* provision.actor[agreementParty].reference -> "612" "Patient"
* provision.actor[agreementParty].reference -> "614" "Vertegenwoordiger"
* provision.actor[agreementParty].reference -> "616" "Zorgverlener"
* provision.code -> "604" "Behandeling"
* dateTime -> "641" "MeestRecenteBespreekdatum"
* sourceReference -> "644" "Wilsverklaring"
* provision.type -> "638" "Afspraak uitzetten ICD (BehandelBesluit)"
* provision.extension[reasonForEnding] -> "643" "RedenBeeindigd"
* provision.period.end -> "642" "DatumBeeindigd"
* provision.actor[agreementParty] -> "646" "AfspraakPartij"
* provision.actor[agreementParty].reference -> "647" "Patient"
* provision.actor[agreementParty].reference -> "649" "Vertegenwoordiger"
* provision.actor[agreementParty].reference -> "651" "Zorgverlener"
* provision.code.text -> "639" "Behandeling van ICD (Behandeling)" 


Instance: F1-ACP-TreatmentDirective-305351004
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 305351004"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d543b9f3-4b87-4f10-bbbb-1425d66f451c"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#305351004 "Admit to ITU"


Instance: F1-ACP-TreatmentDirective-89666000
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 89666000"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "943eff64-86a4-4057-b41c-08a849e244c4"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#89666000 "Cardiopulmonary resuscitation"


Instance: F1-ACP-TreatmentDirective-40617009
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 40617009"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "4db3052d-370a-40e6-b3a8-0c48347747f2"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#40617009 "Artificial respiration"


Instance: F1-ACP-TreatmentDirective-116762002
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 116762002"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d023ee6f-88d6-4a1e-99a7-40118b4cea45"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#116762002 "administration of blood product"


Instance: F1-ACP-TreatmentDirective-281789004
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 281789004"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e2ad3d52-a925-4f82-9c39-e036fc7190a4"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#281789004 "Antibiotic therapy"


Instance: F1-ACP-TreatmentDirective-32485007
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective 32485007"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "23b43ae7-b092-47ef-b992-8c54e716531c"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $snomed#32485007 "Hospital admission"


Instance: F1-ACP-TreatmentDirective-400231000146108
InstanceOf: ACPTreatmentDirective
Title: "F1 ACP TreatmentDirective"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "b56faf40-f7d7-40a8-869e-a5683d0e1004"
* modifierExtension[specificationOther].valueString = "Niet besproken" 
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* status = #active
* dateTime = 2020-10-01
* policy.uri = "https://wetten.overheid.nl/"
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.code = $v3-NullFlavor#OTH
* provision.code.text = "Uitzetten van cardioverter-defibrillator in laatste levensfase (verrichting) (SNOMED CT - 400231000146108)" // 20250710 - This seems now as an OK approach. Created: https://nictiz.atlassian.net/browse/ZIB-2796


Instance: F2-ACP-TreatmentDirective-305351004
InstanceOf: ACPTreatmentDirective
Title: "F2 ACP TreatmentDirective 305351004"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d543b9f3-4b87-4f10-bbbb-1425d66f485c"
* status = #active
* patient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* dateTime = 2022-11-08
* policy.uri = "https://wetten.overheid.nl/"
* provision.type = #permit
* provision.actor[agreementParty][0].reference = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* provision.actor[agreementParty][=].reference.type = "Patient"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* provision.actor[agreementParty][=].reference.type = "PractitionerRole"
* provision.actor[agreementParty][+].reference = Reference(F1-ACP-ContactPerson-MichielHartman) "ContactPerson, Michiel Hartman"
* provision.actor[agreementParty][=].reference.type = "RelatedPerson"
* provision.code = $snomed#305351004 "Admit to ITU"
ValueSet: ACPDesiredPlaceOfDeathVS
Id: ACP-DesiredPlaceDeath
Title: "ACP Desired Place Of Death"
Description: "Valueset for desired place of death"
* insert MetaRules
* $snomed#264362003 "Thuis (omgeving)"
* $snomed#284546000 "Hospice (omgeving)"
* $snomed#108344006 "verpleeghuis en/of locatie voor ambulante zorg (omgeving)"
* $snomed#22232009 "Ziekenhuis (omgeving)"
* $v3-NullFlavor#OTH "Anders"
* $v3-NullFlavor#UNK "Onbekend"

ValueSet: ACPEuthanasiaStatementVS
Id: ACP-EuthanasiaStatement
Title: "ACP Euthanasia Statement"
Description: "What is the patient's position regarding euthanasia and does the patient have a euthanasia statement?"
* insert MetaRules
* $snomed#340181000146102 "heeft euthanasieverklaring (bevinding)"
* $snomed#340191000146100 "heeft geen euthanasieverklaring (bevinding)"
* $snomed#340201000146103 "wil geen euthanasie (bevinding)"
* $v3-NullFlavor#UNK "Onbekend"

ValueSet: MedicalPolicyGoalVS
Id: medical-policy-goal-vs
Title: "Most Important Agreed-upon Goal of Medical Policy"
Description: "A set of codes representing the primary agreed-upon goal of a patient's medical treatment policy."
* insert MetaRules
* $snomed#385987000 "Curatief / actief ziektebeleid"
* $snomed#1351964001 "Life-sustaining treatment (regime/therapy)"
* $snomed#713148004 "Voorkomen en behandelen van symptomen (verrichting)"
* $v3-NullFlavor#UNK "Nog onbekend"


ValueSet: ACPLivingWillTypeVS
Id: ACP-LivingWillType
Title: "ACP Living Will Type"
Description: "What type of living will does the patient have?"
* insert MetaRules
* urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4.14.1#EU "Euthanasieverzoek"
* urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4.14.1#EUD "Euthanasieverzoek met aanvulling Dementie"
* urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4.14.1#LW "Levenswensverklaring"
* urn:oid:2.16.840.1.113883.2.4.3.11.60.40.4.14.1#DO "Verklaring donorschap"

ValueSet: ACPTreatmentTypeVS
Id: ACP-TreatmentType
Title: "ACP Treatment Type"
Description: "Valueset for treatment type"
* insert MetaRules
* include codes from system $snomed
* $snomed#281789004 "Antibiotische therapie (verrichting)"
* $snomed#305351004 "Opname op intensive care (verrichting)"
* $snomed#32485007 "Opname in ziekenhuis (verrichting)"
* $snomed#40617009 "Kunstmatige beademing (verrichting)"
* $snomed#89666000 "Cardiopulmonale resuscitatie (verrichting)"
* $snomed#116762002 "Toediening van bloedproduct (verrichting)"
* $snomed#431415002 "Management of internal defibrillation (procedure)"
// TODO: this code below does not seem correct.
* $snomed#OTH "Overige behandelingen"
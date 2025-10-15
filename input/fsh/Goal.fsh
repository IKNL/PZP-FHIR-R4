Profile: ACPMedicalPolicyGoal
Parent: Goal
Id: ACP-Medical-Policy-Goal
Title: "Medical Policy Goal"
Description: "The primary, agreed-upon goal of a patient's medical treatment policy. Based on Goal resource."
* insert MetaRules
* extension contains
    ExtEncounterReference  named encounter 0..1
* extension[encounter].valueReference only Reference(ACPEncounter) 
* description from MedicalPolicyGoalVS (required)
* subject only Reference(ACPPatient)

Mapping: MapACPMedicalPolicyGoal
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPMedicalPolicyGoal
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "590" "Belangrijkste doel van behandeling ([Meting])"
* -> "591" "Belangrijkste doel van behandeling ([MetingNaam])"
* description -> "592" "Doel ([MetingWaarde])"
* startDate -> "596" "[MeetDatumBeginTijd]"
* note.text -> "598" "[Toelichting]"


Instance: F1-ACP-Medical-Policy-Goal
InstanceOf: ACPMedicalPolicyGoal
Title: "F1 ACP Medical Policy Goal - Life-sustaining treatment"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "a1e0d113-bf6d-4e5c-9bf4-044eda75b709"
* lifecycleStatus = #active
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* description = $snomed#1351964001 "levensverlengende behandeling"
* statusDate = "2020-10-01"
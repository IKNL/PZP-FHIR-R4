Profile: ACPMedicalPolicyGoal
Parent: Goal
Id: ACP-Medical-Policy-Goal
Title: "Medical Policy Goal"
Description: "A profile on the FHIR Goal resource to represent the primary, agreed-upon goal of a patient's medical treatment policy."
* insert MetaRules
* extension contains
    ExtEncounterReference  named encounter 0..1
* extension[encounter].valueReference only Reference(ACPEncounter) 
* description from MedicalPolicyGoalVS (required)
* subject only Reference(Patient)
// TODO would be good to add category code or reference to encounter to distingush the ACP made Goal."

Mapping: MapACPMedicalPolicyGoal
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPMedicalPolicyGoal
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "590" "Belangrijkste doel van behandeling ([Meting])"
* -> "591" "Belangrijkste doel van behandeling ([MetingNaam])"
* description -> "592" "Doel ([MetingWaarde])"
* statusDate -> "596" "[MeetDatumBeginTijd]" // TODO check this if this is ok.
* note.text -> "598" "[Toelichting]"

Instance: F1-ACP-Medical-Policy-Goal
InstanceOf: ACPMedicalPolicyGoal
Title: "F1 ACP Medical Policy Goal - Life-sustaining treatment"
Usage: #example
* extension[encounter].valueReference = Reference(F1-ACP-Encounter-01-10-2020) "Encounter, 2020-10-01"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "a1e0d113-bf6d-4e5c-9bf4-044eda75b709"
* lifecycleStatus = #accepted
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* description = $snomed#1351964001 "Life-sustaining treatment (regime/therapy)"
* statusDate = "2020-10-01"
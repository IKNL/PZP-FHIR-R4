Profile: ACPMedicalPolicyGoal
Parent: Goal
Id: ACP-Medical-Policy-Goal
Title: "ACP Medical Policy Goal"
Description: "A profile on the FHIR Goal resource to represent the primary, agreed-upon goal of a patient's medical treatment policy."
* description from MedicalPolicyGoalVS (required)


Mapping: MapACPMedicalPolicyGoal
Id: pall-izppz-v2025-03-11
Title: "Belangrijkste doel van behandeling ([Meting])"
Source: ACPMedicalPolicyGoal
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "590" "Belangrijkste doel van behandeling ([Meting])"
* description -> "591" "Belangrijkste doel van behandeling ([MetingNaam])"
* statusDate -> "736" "Datum van invullen" // TODO check this if this is ok.


Instance: F1-ACP-Medical-Policy-Goal
InstanceOf: ACPMedicalPolicyGoal
Title: "Medical Policy Goal -Life-sustaining treatment (regime/therapy)"
Usage: #example
* lifecycleStatus = #accepted
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* description = $snomed#1351964001 "Life-sustaining treatment (regime/therapy)"
* statusDate = "2020-10-01"
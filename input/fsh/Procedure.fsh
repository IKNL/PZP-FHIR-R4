Profile: ACDFreedomRestrictingIntervention
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-FreedomRestrictingIntervention
Id: ACP-FreedomRestrictingIntervention
Title: "ACP FreedomRestrictingIntervention"
Description: """Freedom restricting interventions are interventions that are used against the will of the person concerned and that consciously restrict the person's freedom to protect the person or his environment. This definition includes many forms of freedom restriction, such as (not exhaustive)."""
* extension[legallyCapable] 1..1
* code 1..1
* performed[x] ^slicing.discriminator.type = #type
* performed[x] ^slicing.discriminator.path = "$this"
* performed[x] ^slicing.rules = #open
* performedPeriod only Period
* performedPeriod ^sliceName = "performedPeriod"
* performedPeriod.start 1..1


Mapping: MapACDFreedomRestrictingIntervention
Id: pall-izppz-v2025-03-11
Title: "Wilsbekwaamheid (VrijheidsbeperkendeInterventie)"
Source: ACDFreedomRestrictingIntervention
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "431" "Wilsbekwaamheid (VrijheidsbeperkendeInterventie)"
* extension[legallyCapable] -> "432" "Wilsbekwaam" // TODO need to add this inside complex extension on the right sub extension
* extension[legallyCapable] -> "433" "WilsbekwaamToelichting" // TODO need to add this inside complex extension on the right sub extension
* code -> "436" "SoortInterventie"
* performedPeriod.start -> "439" "Begin"
* performedPeriod.end -> "440" "Einde"
* performedDateTime -> "439" "Begin"
* reasonCode -> "437" "RedenVanToepassen"
* reasonReference[legalSituation-LegalStatus] -> "435" "JuridischeSituatie"
* reasonReference[legalSituation-Representation] -> "435" "JuridischeSituatie"
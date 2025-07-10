Profile: ACPFreedomRestrictingIntervention
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-FreedomRestrictingIntervention
Id: ACP-FreedomRestrictingIntervention
Title: "FreedomRestrictingIntervention"
Description: """Freedom restricting interventions are interventions that are used against the will of the person concerned and that consciously restrict the person's freedom to protect the person or his environment. This definition includes many forms of freedom restriction, such as (not exhaustive)."""
* extension[legallyCapable] 1..1
* subject only Reference(ACP-Patient)
// * code 1..1 // TODO -- this is mandatory in zib/dataset but not appicable in in the form.  Check if this should be detached from the zib FreedomRestrictingIntervention? Create a custom extension for this on Patient based on new functional elements?
// Start is mandatory by de zib, but not applicable in the form ?
/*
* performed[x] ^slicing.discriminator.type = #type
* performed[x] ^slicing.discriminator.path = "$this"
* performed[x] ^slicing.rules = #open
* performedPeriod only Period
* performedPeriod ^sliceName = "performedPeriod"
* performedPeriod.start 1..1
*/

Mapping: MapACDFreedomRestrictingIntervention
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPFreedomRestrictingIntervention
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


Instance: F1-ACP-FreedomRestrictingIntervention-Wilsbekwaam
InstanceOf: ACPFreedomRestrictingIntervention
Title: "F1 ACP FreedomRestrictingIntervention Wilsbekwaam"
Usage: #example

* extension[0].extension[0].url = "legallyCapable"
* extension[=].extension[=].valueBoolean = true
* extension[=].url = "http://nictiz.nl/fhir/StructureDefinition/ext-FreedomRestrictingIntervention.LegallyCapable"
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "1dfa6db9-0e94-4338-a91c-f3d20bdbf929"
* status = #completed
* category = $snomed#225317005 "beperking van bewegingsvrijheid"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* subject.type = "Patient"
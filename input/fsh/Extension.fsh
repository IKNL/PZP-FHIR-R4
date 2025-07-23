Extension: ExtLegallyCapableMedicalTreatmentDecisions
Id: ext-LegallyCapable-MedicalTreatmentDecisions
Title: "ext LegallyCapable regarding medical treatment decisions"
Description: "An extension to indicate the patient's legal capacity (LegallyCapable) regarding medical treatment decisions, and to provide a comment on the decisions for which the patient is legally capable."
Context: Patient
* ^purpose = "This extension is based on the [extension FreedomRestrictingIntervention.LegallyCapable](http://nictiz.nl/fhir/StructureDefinition/ext-FreedomRestrictingIntervention.LegallyCapable), but is adapted for the ACP context by allowing its use on the Patient resource and specifying its application to treatment decisions."
* insert MetaRules
* extension ^slicing.discriminator.type = #value
* extension ^slicing.discriminator.path = "url"
* extension ^slicing.rules = #open
* extension ^min = 0
* extension contains
    legallyCapable 0..1 and
    legallyCapableComment 0..1
* extension[legallyCapable].value[x] only boolean
* extension[legallyCapable].value[x] ^short = "LegallyCapable"
* extension[legallyCapable].value[x] ^definition = "Indicates the patient's legal capacity (LegallyCapable) regarding medical treatment decisions."
* extension[legallyCapable].value[x] ^alias = "Wilsbekwaam"
* extension[legallyCapableComment].value[x] only string
* extension[legallyCapableComment].value[x] ^short = "LegallyCapableComment"
* extension[legallyCapableComment].value[x] ^definition = "A comment regarding the patient's legal capacity regarding medical treatment decisions."
* extension[legallyCapableComment].value[x] ^alias = "WilsbekwaamToelichting"

Extension: ExtEncounterReference
Id: ext-EncounterReference
Title: "ext Encounter Reference"
Description: "An extension to link the Encounter during which the Consent, Goal or DeviceUseStatement was created or to which the creation is tightly associated."
Context: Consent, Goal, DeviceUseStatement
* ^purpose = "For some resources it may be important to know the link between the resource and a particular encounter while this is not part of the base resource. This extension allows to link the resource to the Encounter context."
* insert MetaRules
* value[x] only Reference(Encounter)
* value[x] ^short = "Encounter"
* value[x] ^definition = "The Encounter during which this resource was created or to which the creation is tightly associated." 
* value[x] ^comment = "This will typically be the encounter the event occurred within, but some activities may be initiated prior to or after the official completion of an encounter but still be tied to the context of the encounter (e.g. completing the administrative registration after the encounter)."
Extension: ExtLegallyCapableTreatmentDecision
Id: ext-LegallyCapable-TreatmentDecision
Title: "ext LegallyCapable regarding medical treatment decisions"
Description: "An extension to indicate the patient's legal capacity (LegallyCapable) regarding medical treatment decisions, and to provide a comment on the decisions for which the patient is legally capable."
Context: Patient
* ^purpose = "This extension is based on the [extension FreedomRestrictingIntervention.LegallyCapable](http://nictiz.nl/fhir/StructureDefinition/ext-FreedomRestrictingIntervention.LegallyCapable), but is adapted for the ACP context by allowing its use on the Patient resource and specifying its application to treatment decisions."
* insert MetaRules
* obeys ACP-LegallyCapable-1
* extension ^slicing.discriminator.type = #value
* extension ^slicing.discriminator.path = "url"
* extension ^slicing.rules = #open
* extension ^min = 0
* extension contains
    legallyCapable 0..1 and
    legallyCapableComment 0..1
* extension[legallyCapable] ^condition = "ACP-LegallyCapable-1"
* extension[legallyCapable].value[x] only boolean
* extension[legallyCapable].value[x] ^short = "LegallyCapable"
* extension[legallyCapable].value[x] ^definition = "Indicates the patient's legal capacity (LegallyCapable) regarding medical treatment decisions."
* extension[legallyCapable].value[x] ^alias = "Wilsbekwaam"
* extension[legallyCapable].value[x] ^condition = "ACP-LegallyCapable-1"
* extension[legallyCapableComment] ^condition = "ACP-LegallyCapable-1"
* extension[legallyCapableComment].value[x] only string
* extension[legallyCapableComment].value[x] ^short = "LegallyCapableComment"
* extension[legallyCapableComment].value[x] ^definition = "A comment regarding the patient's legal capacity regarding medical treatment decisions."
* extension[legallyCapableComment].value[x] ^alias = "WilsbekwaamToelichting"
* extension[legallyCapableComment].value[x] ^condition = "ACP-LegallyCapable-1"

Invariant: ACP-LegallyCapable-1
Description: "If the patient is not legally capable, an explanation must be provided" // TODO check if we want to keep this invariant (this is a copy of the original invariant from the FreedomRestrictingIntervention.LegallyCapable extension)
* severity = #warning
* expression = "extension.where(url='legallyCapable').value = false implies extension.where(url='legallyCapableComment').value.exists()"

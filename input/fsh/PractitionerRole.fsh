Profile: ACPPractitionerRole
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole
Id: ACP-PractitionerRole
Title: "ACP Practitioner Role"
Description: "[TO-DO]"
* insert MetaRules
* code ^mustSupport = false
* code.coding.system MS
* code.coding.code MS
* specialty[specialty] ^sliceName = "specialty"
* specialty[specialty] ^mustSupport = true

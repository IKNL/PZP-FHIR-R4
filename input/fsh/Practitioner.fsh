
Profile: ACPPractitioner
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner
Id: ACP-Practitioner
Title: "ACP Practitioner"
Description: "[TO-DO]"
* insert MetaRules
* . ^short = "HealthProfessional, Gesprek gevoerd door"
* . ^comment = "[TO-DO] In the context of Advance Care Planning (ACP), a Practitioner refers to a healthcare professional who engages in discussions and makes agreements with the Patient and/or their Legal Representative. Depending on the specific stage or pathway of the ACP process, multiple Practitioners may be involved, each responsible for facilitating conversations and documenting decisions in accordance with their role."
* identifier[uzi] ^sliceName = "uzi"
* identifier[uzi] ^mustSupport = true
* identifier[agb] ^sliceName = "agb"
* identifier[agb] ^mustSupport = true
* name[nameInformation] ^sliceName = "nameInformation"
* name[nameInformation].family.extension[prefix] ^sliceName = "prefix"
* name[nameInformation].family.extension[prefix] ^mustSupport = true
* name[nameInformation].family.extension[lastName] ^sliceName = "lastName"
* name[nameInformation].family.extension[lastName] ^mustSupport = true
* name.given MS
Profile: ACPHealthProfessionalPractitionerRole
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole
Id: ACP-HealthProfessional-PractitionerRole
Title: "HealthProfessional PractitionerRole"
Description: "A health professional is a person who is authorized to perform actions in the field of individual healthcare."
* insert MetaRules
* practitioner only Reference(ACPHealthProfessionalPractitioner)
* specialty[specialty] ^sliceName = "specialty"
* specialty[specialty] ^mustSupport = true


Mapping: MapACPHealthProfessionalPractitionerRole
Id: pall-izppz-v2025-03-11
Title: "Gesprek gevoerd door (Zorgverlener)"
Source: ACPHealthProfessionalPractitionerRole
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* specialty[specialty]  -> "405" "Specialisme"
// TODO "430" "ZorgverlenerRol" is not yet implemented in the Nictiz FHIR profiles, because this is mapped in the resources that refer to the PractitionerRole. It is not mapped in PractitionerRole.code. Decide what to do.


Instance: F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "F1 ACP HealthProfessional PractitionerRole Dr. van Huissen"
Usage: #example
* practitioner = Reference(F1-ACP-HealthProfessional-Practitioner-DrVanHuissen) "Healthcare professional (person), van Huissen"
* practitioner.type = "Practitioner"
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"
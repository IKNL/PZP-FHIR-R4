Profile: ACPHealthProfessionalPractitionerRole
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole
Id: ACP-HealthProfessional-PractitionerRole
Title: "HealthProfessional PractitionerRole"
Description: "A health professional is a person who is authorized to perform actions in the field of individual healthcare."
* insert MetaRules
* practitioner only Reference(ACPHealthProfessionalPractitioner)


Mapping: MapACPHealthProfessionalPractitionerRole
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPHealthProfessionalPractitionerRole
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* -> "617" "Zorgverlener"
* -> "636" "Zorgverlener"
* -> "652" "Zorgverlener"
* specialty[specialty]  -> "405" "Specialisme"


Instance: F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "F1 ACP HealthProfessional PractitionerRole Dr. van Huissen"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ff6d8146-1014-4ef4-9645-e8207364c942"
* practitioner = Reference(F1-ACP-HealthProfessional-Practitioner-DrVanHuissen) "Healthcare professional (person), van Huissen"
* practitioner.type = "Practitioner"
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"
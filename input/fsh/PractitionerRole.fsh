Profile: ACPHealthProfessionalPractitionerRole
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole
Id: ACP-HealthProfessional-PractitionerRole
Title: "HealthProfessional PractitionerRole"
Description: "The specialty of a person who is authorized to perform actions in the field of individual healthcare. Based on nl-core-HealthProfessionalPractitionerRole and HCIM HealthProfessional."
* insert MetaRules
* practitioner only Reference(ACPHealthProfessionalPractitioner)

* insert ObligationRules(practitioner)
* insert ObligationRules(specialty[specialty])

Mapping: MapACPHealthProfessionalPractitionerRole
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPHealthProfessionalPractitionerRole
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
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
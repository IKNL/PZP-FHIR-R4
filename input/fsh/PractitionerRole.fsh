Profile: ACPHealthProfessionalPractitionerRole
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole
Id: ACP-HealthProfessional-PractitionerRole
Title: "ACP HealthProfessional PractitionerRole"
Description: "The specialty of a person who is authorized to perform actions in the field of individual healthcare. Based on nl-core-HealthProfessionalPractitionerRole and HCIM HealthProfessional."
* insert MetaRules
* practitioner only Reference(ACPHealthProfessionalPractitioner)

* insert ObligationRules(practitioner)
* insert ObligationRules(specialty[specialty])

Mapping: MapACPHealthProfessionalPractitionerRole
Id: pall-izppz-zib2020v2026-02-24
Title: "ACP dataset"
Source: ACPHealthProfessionalPractitionerRole
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2026-05-12T07:58:08"
* -> "391" "Gesprek gevoerd door (Zorgverlener)"
* -> "617" "Zorgverlener"
* -> "636" "Zorgverlener"
* -> "652" "Zorgverlener"
* specialty[specialty]  -> "405" "Specialisme"


Instance: ACP-HealthProfessional-PractitionerRole-DrVanHuissen-Pat1
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "ACP HealthProfessional PractitionerRole - Dr. van Huissen - Pat 1"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ff6d8146-1014-4ef4-9645-e8207364c942"
* practitioner = Reference(ACP-HealthProfessional-Practitioner-DrVanHuissen-Pat1) "Healthcare professional (person), van Huissen"
* practitioner.type = "Practitioner"
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"


Instance: ACP-HealthProfessional-PractitionerRole-DesireeWolters-Pat2
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "ACP HealthProfessional PractitionerRole - Desiree Wolters - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c69d5830-1304-4a4e-bb37-49043282efa3"
* practitioner = Reference(ACP-HealthProfessional-Practitioner-DesireeWolters-Pat2) "Healthcare professional (person), Desiree Wolters"
* practitioner.type = "Practitioner"
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"


Instance: ACP-HealthProfessional-PractitionerRole-Santos-Pat2
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "ACP HealthProfessional PractitionerRole - Santos - Pat 2"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e38a934b-2f66-4ae4-954d-f1aee1d8f378"
* practitioner = Reference(ACP-HealthProfessional-Practitioner-Santos-Pat2) "Healthcare professional (person), Santos"
* practitioner.type = "Practitioner"
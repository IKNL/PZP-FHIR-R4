Instance: P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters
InstanceOf: ACP-HealthProfessional-PractitionerRole
Title: "P2 ACP HealthProfessional PractitionerRole Desiree Wolters"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "c69d5830-1304-4a4e-bb37-49043282efa3"
* practitioner = Reference(P2-ACP-HealthProfessional-Practitioner-DesireeWolters) "Healthcare professional (person), Desiree Wolters"
* practitioner.type = "Practitioner"
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"


Instance: P2-ACP-HealthProfessional-PractitionerRole-Santos
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "P2 ACP HealthProfessional PractitionerRole Santos"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "e38a934b-2f66-4ae4-954d-f1aee1d8f378"
* practitioner = Reference(P2-ACP-HealthProfessional-Practitioner-Santos) "Healthcare professional (person), Santos"
* practitioner.type = "Practitioner"
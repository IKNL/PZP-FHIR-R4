Instance: P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "P1 ACP HealthProfessional PractitionerRole Dr. van Huissen"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "f02aa6d0-f7b8-4bc6-a9d7-2c169ae7ace5"
* practitioner = Reference(P1-ACP-HealthProfessional-Practitioner-DrVanHuissen) "Healthcare professional (person), van Huissen"
* practitioner.type = "Practitioner" 
* specialty.coding.version = "2020-10-23T00:00:00"
* specialty.coding = urn:oid:2.16.840.1.113883.2.4.6.7#0100 "Huisartsen, niet nader gespecificeerd"


Instance: P1-ACP-HealthProfessional-PractitionerRole-Santos
InstanceOf: ACPHealthProfessionalPractitionerRole
Title: "P1 ACP HealthProfessional PractitionerRole Santos"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "cdafd4b4-47ff-4e04-9f99-51f922b05152"
* practitioner = Reference(P1-ACP-HealthProfessional-Practitioner-Santos) "Healthcare professional (person), Santos"
* practitioner.type = "Practitioner"



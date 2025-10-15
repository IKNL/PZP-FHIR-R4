Profile: ACPCommunication
Parent: Communication
Id: ACP-Communication
Title: "Communication"
Description: "Communication events that have taken place in context of Advance Care Planning. Based on Communication resource."
* insert MetaRules
* topic ^comment = "For information patient about own responsibility the following text may be added to the `topic.text` element: Informing the patient about their own responsibility to discuss these treatment agreements with relatives."
* subject only Reference(ACPPatient)
* recipient only Reference(ACPPatient)
* sender only Reference(ACPHealthProfessionalPractitionerRole)
* sent ^comment = "Indicate the date and preferrably time when the communication was sent"
* reasonCode 1..1
* reasonCode = $snomed#713603004 // "Advance care planning (procedure)"


Mapping: MapACPCommunication
Id: pall-izppz-zib2020v2025-03-11
Title: "PZP dataset"
Source: ACPCommunication
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/scenarios/scenarios/2.16.840.1.113883.2.4.3.11.60.117.4.14/2025-08-05T00:00:00"
* -> "734" "Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken?"


Instance: F1-ACP-Communication-01-10-2020
InstanceOf: ACPCommunication
Title: "F1 ACP Communication"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "dd6d7146-1014-4ef4-9145-e8207364c942"
* topic = $snomed#223449006 "Recommendation to inform someone (procedure)"
* topic.text = "Informing the patient about their own responsibility to discuss these treatment agreements with relatives."
* status = #completed
* sent = "2020-10-01"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* recipient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* sender = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* reasonCode = $snomed#713603004 "Advance care planning (procedure)"
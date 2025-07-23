Profile: ACPCommunication
Parent: Communication
Id: ACP-Communication
Title: "Communication"
Description: "Profile that defines communication events that have taken place in context of Advance Care Planning."
* insert MetaRules
* topic ^comment =  "For information patient about own responsibility the following text may be added to the `topic.text` element: Informing the patient about their own responsibility to discuss these treatment agreements with relatives." // TODO add code here?
* subject only Reference(ACPPatient)
* recipient only Reference(ACPPatient)
* sender only Reference(ACPHealthProfessionalPractitionerRole)
* reasonCode 1..1
* reasonCode = $snomed#713603004 "Advance care planning (procedure)"

Mapping: MapACPCommunication
Id: pall-izppz-v2025-03-11
Title: "PZP dataset"
Source: ACPCommunication
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "734" "Heeft u patient geïnformeerd over eigen verantwoordelijkheid om deze behandelafspraken met naasten te bespreken?"

Instance: F1-ACP-Communication-01-10-2020
InstanceOf: ACPCommunication
Title: "F1 ACP Communication"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "dd6d7146-1014-4ef4-9645-e8207364c942"
* topic = $snomed#223449006 "Recommendation regarding contacting someone (procedure)"
* topic.text = "Informing the patient about their own responsibility to discuss these treatment agreements with relatives."
* status = #completed
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* recipient = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* sender = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"

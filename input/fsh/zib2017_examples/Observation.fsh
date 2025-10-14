Instance: P1-ACP-SpecificCareWishes
InstanceOf: ACPSpecificCareWishes
Title: "P1 ACP Specific Care Wishes"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d2a5de51-c409-4ade-846a-9b81d1f29a26"
* status = #final
* code =  $snomed#153851000146100 "wensen en verwachtingen met betrekking tot uitkomst van behandeling (waarneembare entiteit)"
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* valueString = "Broer Michiel is erg betrokken bij het proces van Hendrik. Het gaat de laatste tijd een stuk slechter en Hendrik denkt vaker na over de dood. Hij is niet bang, maar vindt het lastig om zijn familie achter te laten."
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg (verrichting)" 


Instance: P1-ACP-PreferredPlaceOfDeath-Home
InstanceOf: ACPPreferredPlaceOfDeath
Title: "P1 ACP Preferred Place Of Death Home"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "253b44be-bfad-4ad6-a1d6-2011f1db8a98"
* status = #final
* code =  $snomed#395091006 
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#264362003 "thuis (omgeving)"
* note.text = "Het liefst rustig thuis"


Instance: P1-ACP-PositionRegardingEuthanasia-No
InstanceOf: ACPPositionRegardingEuthanasia
Title: "P1 ACP Position Regarding Euthanasia No"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d3269776-a4dd-4f77-835e-9a17f5fb048b"
* status = #final
* code =  $snomed#340171000146104 
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#340201000146103 "Wenst geen euthanasie"


Instance: P1-ACP-OrganDonationChoiceRegistration-Yes
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "P1 ACP Donor Registration Yes"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "ec6d52d0-4ebc-4904-bf8b-8610d049be24"
* status = #final
* code = $snomed#570801000146104 "geregistreerd in orgaan donorregister (bevinding)" 
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* valueCodeableConcept = $snomed#373066001


Instance: P1-ACP-OtherImportantInformation
InstanceOf: ACPOtherImportantInformation
Title: "P1 ACP Other Important Information"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "8d2ba0a3-1a15-4066-9d6a-af596c826cbe"
* status = #final
* code =  $snomed#247751003 
* subject = Reference(P1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* encounter = Reference(P1-ACP-Encounter-29-07-2025) "Encounter, 2025-07-29"
* effectiveDateTime = "2025-07-29"
* performer = Reference(P1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* valueString = "Hendrik wordt erg vrolijk van tulpen"

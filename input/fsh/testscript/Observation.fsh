Instance: P2-ACPSpecificCareWishes
InstanceOf: ACPSpecificCareWishes
Title: "P2 ACP Specific Care Wishes"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "171c806c-a4bf-4b1e-a7d4-497e9ed44278"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* performer = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#153851000146100
* valueString = "De kleinzoon van mevrouw van der Sluijs is geboren en mevrouw is dolgelukkig dat ze hem heeft kunnen zien. Ze merkt dat ze fysiek erg achteruitgaat. Mevrouw heeft daar nu vrede mee, in tegenstelling tot eerdere gesprekken."
* effectiveDateTime = "2025-08-07"
* method = $snomed#370819000 "vaststellen van persoonlijke waarden en wensen met betrekking tot zorg (verrichting)"

Instance: P2-ACPPreferredPlaceOfDeath
InstanceOf: ACPPreferredPlaceOfDeath
Title: "P2 ACP Preferred Place Of Death"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "d1866b00-aa64-4155-aa20-25ce51dac894"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* performer = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#395091006
* effectiveDateTime = "2025-08-07"
* valueCodeableConcept = $snomed#264362003 "Private dwelling"
* note.text = "Het liefst rustig thuis"

Instance: P2-ACPPositionRegardingEuthanasia
InstanceOf: ACPPositionRegardingEuthanasia
Title: "P2 ACP Position Regarding Euthanasia"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "1e73ad4f-6822-412e-a8e1-8a9f235e5a54"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* performer = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#340171000146104
* valueCodeableConcept = $snomed#340201000146103 "Wil geen euthanasie (bevinding)"
* effectiveDateTime = "2025-08-07"

Instance: P2-ACPOrganDonationChoiceRegistration
InstanceOf: ACPOrganDonationChoiceRegistration
Title: "P2 ACP Organ Donation Choice Registration"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "856791c1-91cf-404a-ab2e-e1ed05c7c880"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* performer = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#570801000146104 "geregistreerd in orgaan donorregister (bevinding)"
* valueCodeableConcept = $snomed#373066001 "ja"
* effectiveDateTime = "2025-08-07"

Instance: P2-ACPOtherImportantInformation
InstanceOf: ACPOtherImportantInformation
Title: "P2 ACP Other Important Information"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "45ff425e-5c09-4930-b4ea-3819dc857734"
* encounter = Reference(P2-ACP-Encounter-07-08-2025) "Encounter, 2025-08-07"
* subject = Reference(P2-ACP-Patient-Samiravandersluijs) "Patient, Samira van der Sluijs"
* performer = Reference(P2-ACP-HealthProfessional-PractitionerRole-DesireeWolters) "Healthcare professional (role), Desiree Wolters"
* status = #final
* code =  $snomed#247751003
* valueString = "Mevrouw is gek op haar kleinzoon, dus brengt graag veel tijd met hem door."
* effectiveDateTime = "2025-08-07"



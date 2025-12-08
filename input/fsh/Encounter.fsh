Profile: ACPEncounter
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-Encounter
Id: ACP-Encounter
Title: "Encounter"
Description: "Any interaction, regardless of the situation, between a patient and the healthcare provider, in which the healthcare provider has primary responsibility for diagnosing, evaluating and treating the patient’s condition and informing the patient. These can be visits, appointments or non face-to-face interactions. Based on nl-core-Encounter and HCIM Encounter."
* insert MetaRules
* subject only Reference(ACPPatient)
* participant ^slicing.discriminator.type = #profile
* participant ^slicing.discriminator.path = "individual.resolve()"
* participant ^slicing.rules = #open
* participant contains 
    contactPerson 0..*
* participant[healthProfessional].individual only Reference(ACPHealthProfessionalPractitionerRole)
* participant[healthProfessional].individual ^comment = "Each occurrence of the zib HealthProfessional is normally represented by _two_ FHIR resources: a PractitionerRole resource (instance of [nl-core-HealthProfessional-PractitionerRole](http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-PractitionerRole)) and a Practitioner resource (instance of [nl-core-HealthProfessional-Practitioner](http://nictiz.nl/fhir/StructureDefinition/nl-core-HealthProfessional-Practitioner)). The Practitioner resource is referenced from the PractitionerRole instance. For this reason, sending systems should fill the reference to the PractitionerRole instance here, and not the Practitioner resource. Receiving systems can then retrieve the reference to the Practitioner resource from that PractitionerRole instance.\r\n\r\nIn rare circumstances, there is only a Practitioner instance, in which case it is that instance which can be referenced on the `Encounter.participant` element (due to open slicing). Since this should be the exception, the nl-core-HealthProfessional-Practitioner profile is not explicitly mentioned as a target profile."
* participant[contactPerson].individual only Reference(ACPContactPerson)
// Patient is not allowed like this.... in R5 it will be.* participant[patient].individual only Reference(ACPPatient) --> Patient is set in .subject.

* insert ObligationRules(subject)
* insert ObligationRules(participant[contactPerson])
* insert ObligationRules(participant[healthProfessional])
* insert ObligationRules(period.start)
* insert ObligationRules(reasonReference[procedure])
* insert ObligationRules(reasonReference.extension[commentContactReason])
* insert ObligationRules(reasonCode[deviatingResult].extension[commentContactReason])


Mapping: MapACPEncounter
Id: pall-izppz-zib2020v2025-03-11
Title: "ACP dataset"
Source: ACPEncounter
Target: "https://decor.nictiz.nl/exist/apps/api/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10%3A37%3A48/$view?language=nl-NL&ui=nl-NL&format=html&hidecolumns=3456gh&release=2025-10-29T13%3A09%3A23"
* -> "808" "Contact"
* class -> "809" "ContactType"
* subject -> "514" "Gesprek gevoerd in bijzijn van (Patient)" // In R5 patient is added to .participant.individual. For now, if present at .subject, we assume the patient was present. Also clear from the definition of the subject element: "The patient or group present at the encounter" 
* participant -> "810" "ContactMet"
* participant[contactPerson].individual -> "554" "Gesprek gevoerd in bijzijn van (Contactpersoon)"
* participant[healthProfessional].individual -> "842" "Gesprek gevoerd door (Zorgverlener)"
* period.start -> "814" "BeginDatumTijd"
* period.start -> "736" "Datum van invullen"
* reasonReference[procedure] -> "819" "Verrichting"
* reasonReference.extension[commentContactReason] -> "822" "ToelichtingRedenContact"
* reasonCode[deviatingResult].extension[commentContactReason] -> "822" "ToelichtingRedenContact"


Instance: F1-ACP-Encounter-01-10-2020
InstanceOf: ACPEncounter
Title: "F1 ACP Encounter 01-10-2020"
Usage: #example
* identifier.type = $v2-0203#RI "Resource identifier"
* identifier.system = "https://acme.com/fhir/NamingSystem/resource-business-identifier"
* identifier.value = "64627bfa-a127-4d3a-8187-39426d7937dc"
* status = #finished
* class = $v3-ActCode#IMP "inpatient encounter"
* subject = Reference(F1-ACP-Patient-HendrikHartman) "Patient, Hendrik Hartman"
* participant[0].individual = Reference(F1-ACP-HealthProfessional-PractitionerRole-DrVanHuissen) "Healthcare professional (role), van Huissen"
* participant[=].individual.type = "PractitionerRole"
* participant[+].individual = Reference(F1-ACP-ContactPerson-MichielHartman) "ContactPerson, Michiel Hartman"
* participant[=].individual.type = "RelatedPerson"
* period.start = "2020-10-01"
* period.end = "2020-10-01"
* reasonReference = Reference(F1-ACP-Procedure-01-10-2020) "Procedure, ACP"
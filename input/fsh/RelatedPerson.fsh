
Profile: ACPContactPerson
Parent: http://nictiz.nl/fhir/StructureDefinition/nl-core-ContactPerson
Id: ACP-ContactPerson
Title: "ACP ContactPerson"
Description: "A contact is a person not being a healthcare professional who is involved in the patient’s care, such as family members, caregivers, mental caretakers, guardians and legal representatives."
* insert MetaRules
// Name is not mandatory here.
* relationship 1..*
* relationship[role] ^sliceName = "role"
* relationship[role] 1..1



Mapping: MapACPContactPerson
Id: pall-izppz-v2025-03-11
Title: "Wettelijk vertegenwoordiger (Contactpersoon)"
Source: ACPContactPerson
Target: "https://decor.nictiz.nl/ad/#/pall-izppz-/datasets/dataset/2.16.840.1.113883.2.4.3.11.60.117.1.1/2020-07-29T10:37:48/concept/2.16.840.1.113883.2.4.3.11.60.117.2.350/2025-03-11T13:43:38"
* -> "441" "Wettelijk vertegenwoordiger (Contactpersoon)"
* name -> "442" "Naamgegevens"
// TODO: decide if we want to go into providing mappings inside these data type profiles. 
* telecom -> "454" "Contactgegevens"
* address -> "463" "Adresgegevens"
* relationship[role] -> "475" "Adresgegevens"
* relationship[relationship] -> "476" "Relatie"